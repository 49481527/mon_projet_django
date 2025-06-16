from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from expenses.models import Expense, Category
from django.db.models import Sum, Count
import json
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import login
from .forms import SignUpForm


def profile_view(request):
    user = request.user
    
    expenses = Expense.objects.filter(user=user)
    total_expenses = expenses.count()
    total_expenses_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_balance = -total_expenses_amount  # Puisqu'il n'y a pas de revenus
    
    join_date = user.date_joined
    months_since_join = max(1, (timezone.now().year - join_date.year) * 12 + 
                          (timezone.now().month - join_date.month))
    monthly_average = round(total_expenses_amount / months_since_join, 2)
    
    categories = Category.objects.filter(user=user).annotate(
        total=Sum('expenses__amount'),
        count=Count('expenses')
    ).order_by('-total')[:5]
    
    category_styles = [
        {'color': 'danger', 'icon': 'fa-utensils'},
        {'color': 'warning', 'icon': 'fa-car'},
        {'color': 'info', 'icon': 'fa-gamepad'},
        {'color': 'success', 'icon': 'fa-home'},
        {'color': 'primary', 'icon': 'fa-shopping-bag'},
    ]
    
    for i, category in enumerate(categories):
        if total_expenses_amount > 0:
            category.percentage = round((category.total or 0) / total_expenses_amount * 100)
        else:
            category.percentage = 0
        style = category_styles[i % len(category_styles)]
        category.color = style['color']
        category.icon = style['icon']
    
    recent_transactions = Expense.objects.filter(user=user).order_by('-date')[:5]
    
    monthly_data = []
    monthly_labels = []
    for i in range(6, -1, -1):
        month = timezone.now() - timedelta(days=30*i)
        monthly_labels.append(month.strftime("%b %Y"))
        monthly_expenses = Expense.objects.filter(
            user=user,
            date__year=month.year,
            date__month=month.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_data.append(float(monthly_expenses))
    
    context = {
        'user': user,
        'total_balance': total_balance,
        'total_expenses': total_expenses,
        'monthly_average': monthly_average,
        'categories': categories,
        'recent_transactions': recent_transactions,
        'monthly_data': json.dumps(monthly_data),
        'monthly_labels': json.dumps(monthly_labels),
    }
    
    return render(request, 'users/profile.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Connecte automatiquement
            messages.success(request, "Bienvenue ! Vous êtes maintenant connecté.")
            return redirect('users:profile')  # ✅ Redirige vers la page de profil
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
