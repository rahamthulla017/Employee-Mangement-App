from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView
from .forms import SignUpForm, UserUpdateForm
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'manager':
        return redirect('manager_dashboard')
    elif user.role == 'employee':
        return redirect('employee_dashboard')
    return redirect('login')

def is_admin(user):
    return user.role == 'admin'

def is_manager(user):
    return user.role == 'manager' or user.role == 'admin' # Managers usually have access to what employees have, but maybe not admin. Admin has everything? prompt says "Manager cannot access Admin panel".

def is_employee(user):
    return user.role == 'employee'

from tasks.models import Project, Task

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'projects_count': Project.objects.count(),
        'users_count': User.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    return render(request, 'accounts/manager_dashboard.html')

@login_required
def employee_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user, status='pending')
    context = {
        'tasks': tasks,
        'tasks_count': tasks.count(),
    }
    return render(request, 'accounts/employee_dashboard.html', context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user
