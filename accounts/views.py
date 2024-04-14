from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = [
        'date_of_birth',
        'description',
        'sports',
        'avatar'
    ]
    template_name = 'users/update_user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in_user_id'] = self.request.user.id
        context['profile_owner_id'] = self.object.id
        return context

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user_profile', kwargs={'pk': user_id})