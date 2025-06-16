from django.urls import path
from .views import signup_view, profile_view
from django.contrib.auth import views as auth_views

app_name = 'users'  # ✅ obligatoire ici pour le namespace 'users' de include()

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view,name='profile'),
]
