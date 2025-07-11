from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import FinanceEntry
from .forms import FinanceEntryForm, signupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import re
from datetime import datetime


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # If the user is authenticated, redirect to the finance entries page
        return redirect('dashboard')  # Assuming you have a dashboard view
    # If the user is not authenticated, render the home page
    return render(request, 'tracker/home.html')

@login_required
def dashboard(request):
    # This view will be accessible only to authenticated users
    incomes=FinanceEntry.objects.filter(user=request.user, entry_type='INCOME')
    expenses=FinanceEntry.objects.filter(user=request.user, entry_type='EXPENSE')
    return render(request, 'tracker/dashboard.html', {
        'incomes': incomes,
        'expenses': expenses,
    })

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = FinanceEntryForm(request.POST)
        if form.is_valid():
            finance_entry = form.save(commit=False)
            finance_entry.user = request.user
            finance_entry.save()
            return redirect('dashboard')
    else:
        form = FinanceEntryForm()
    return render(request, 'tracker/add_entry.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# tracker/views.py

def parse_bill_text(text):
    entry_type = 'expenditure'
    category = 'Food'
    amount = 0.0

    # Extract date from known line pattern
    date_match = re.search(r'Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{2})', text)
    date_str = date_match.group(1) if date_match else '01/01/00'
    date_time = datetime.strptime(date_str, '%d/%m/%y')

    # Split text into lines for smarter scanning
    lines = text.splitlines()

    # Go from bottom up and find the largest number
    amounts = []
    for line in reversed(lines):
        numbers = re.findall(r'\d{2,5}[.,]?\d{0,2}', line)
        for num in numbers:
            try:
                val = float(num.replace(',', '.'))
                if val > 0:
                    amounts.append(val)
            except:
                pass

    if amounts:
        # Take the maximum amount found (usually grand total)
        amount = max(amounts)

    return {
        'entry_type': entry_type,
        'amount': amount,
        'category': category,
        'date_time': date_time,
    }

def extract_bill_text_view(request):
    if request.method == 'POST' and request.FILES['bill_image']:
        image = request.FILES['bill_image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)

        # OCR.space API call
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data={
                    'apikey': 'helloworld',  # demo key
                    'language': 'eng',
                }
            )
        result = response.json()
        extracted_text = result['ParsedResults'][0]['ParsedText']

        # ⬇️ Use our parser function here
        parsed = parse_bill_text(extracted_text)
        return render(request, 'tracker/bill_review.html', {
            'text': extracted_text,
            'parsed': parsed
        })

    return render(request, 'tracker/upload_bill.html')
