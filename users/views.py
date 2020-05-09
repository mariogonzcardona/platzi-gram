"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView,FormView,UpdateView
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from posts.models import Post
from users.models import Profile
from django.contrib.auth import views as auth_views

# Forms
from users.forms import SignupForm

class UserDetailView(LoginRequiredMixin,DetailView):
    """User detail view."""

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class SignupView(FormView):
    template_name='users/signup.html'
    form_class=SignupForm
    success_url=reverse_lazy('users:login')

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin,UpdateView):
    template_name='users/update_profile.html'
    model=Profile
    fields=['website','phone_number','biography','picture']
    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        username=self.object.user.username
        return reverse('users:detail',kwargs={'username':username})

class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    template_name='users/logout.htlm'

@login_required
def logout_view(request):
    """Logout a user."""
    logout(request)
    return redirect('users:login')