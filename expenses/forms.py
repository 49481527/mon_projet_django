from django import forms
from .models import Expense  # Assure-toi que le modèle Expense existe bien

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']  # à adapter selon ton modèle
        
