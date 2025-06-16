from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm  # À créer si tu ne l’as pas
from django.utils import timezone
from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404, redirect





@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:transaction_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def transaction_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/transaction_list.html', {'expenses': expenses})



def home(request):
    return render(request, 'expenses/home.html')

def transaction_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    average_expense = expenses.aggregate(Avg('amount'))['amount__avg'] or 0
    return render(request, 'expenses/transaction_list.html', {
        'expenses': expenses,
        'total_expense': int(total_expense),
        'average_expense': int(average_expense),
    })

def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses:expense_list')  # adapte à ton nom d’URL de liste des dépenses
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

    
@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses:transaction_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {'form': form})
