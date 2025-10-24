from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from hn_jobs.utils import add_users_context, get_tjalerts_logger
from jobs.models import Alert

from .models import CustomUser

logger = get_tjalerts_logger(__name__)


class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = CustomUser
    fields = ["name", "email"]
    success_message = "User Profile Updated"
    success_url = reverse_lazy("settings")
    template_name = "account/settings.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        add_users_context(context, user, self)

        context["alerts"] = Alert.objects.filter(email=user.email)

        return context


def resend_email_confirmation_email(request):
    user = request.user

    adapter = get_adapter(request)
    emailaddress = EmailAddress.objects.get_for_user(user, user.email)

    adapter.send_confirmation_mail(request, emailaddress, signup=False)

    return redirect("settings")
