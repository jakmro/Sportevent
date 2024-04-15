from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from django.http import Http404
from django.utils.translation import gettext


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

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user_profile', kwargs={'pk': user_id})

    def get_object(self, queryset=None):
        obj = super(UpdateProfileView, self).get_object(queryset)
        if obj != self.request.user:
            raise Http404(
                gettext("You don't own this profile")
            )
        return obj


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('home')
    template_name = 'users/delete_user_profile.html'

    def get_object(self, queryset=None):
        obj = super(DeleteProfileView, self).get_object(queryset)
        if obj != self.request.user:
            raise Http404(
                gettext("You don't own this profile")
            )
        return obj
