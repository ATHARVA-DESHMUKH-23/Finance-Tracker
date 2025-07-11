from django.db import models
from django.contrib.auth.models import User

class FinanceEntry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expenditure'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.entry_type} - {self.amount}"
# Create your models here.
