from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.utils.translation import gettext
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from ics import Calendar, Event as IcsEvent
from .utils import email_verification_token
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from events.models import Meeting, EventRegistration


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('email_verification')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_verification_email(self.request, self.object)
        return response


def send_verification_email(request, user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    verify_url = f'http://{domain}{link}'
    send_mail(
        'Verify your email address',
        f'Follow this link to verify your email address: {verify_url}',
        None,
        [user.email]
    )


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect('email_verified')
    else:
        return redirect('email_verification_error')


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.get_object().id
        subscription_link = self.request.build_absolute_uri(reverse('user_calendar', kwargs={'pk': pk}))
        context['subscription_link'] = subscription_link
        return context


def user_calendar(request, pk):
    user = CustomUser.objects.get(pk=pk)
    registrations = EventRegistration.objects.filter(user=user)
    calendar = Calendar()
    for registration in registrations:
        event = registration.event
        meetings = Meeting.objects.filter(event=event)
        for meeting in meetings:
            ics_event = IcsEvent()
            ics_event.name = event.name
            ics_event.begin = meeting.start_datetime
            ics_event.end = meeting.end_datetime
            ics_event.description = event.description
            ics_event.location = event.facility.name
            ics_event.categories = event.sport_type
            calendar.events.add(ics_event)

    response = HttpResponse(str(calendar), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="user_calendar.ics"'

    return response


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/update_user_profile.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user_profile', kwargs={'pk': user_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404(
                gettext("You don't own this profile")
            )
        return obj

    def form_valid(self, form):
        if form.cleaned_data['email'] != self.request.user.email:
            form.instance.email_verified = False
            response = super().form_valid(form)
            send_verification_email(self.request, self.object)
            return response
        return super().form_valid(form)


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('home')
    template_name = 'users/delete_user_profile.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404(
                gettext("You don't own this profile")
            )
        return obj
