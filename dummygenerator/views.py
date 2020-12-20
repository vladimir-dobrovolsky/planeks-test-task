from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.views.generic import RedirectView

from .models import FakeCSVSchema, FakeCSVSchemaColumn

# Create your views here.

UserModel = get_user_model()


class HomeRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("home")


class HomepageView(TemplateView):
    template_name = "dummygenerator/home.html"
    extra_context = {"page_title": "Home"}


class Login(LoginView):
    template_name = "dummygenerator/registration/login.html"


class Logout(LogoutView):
    template_name = "dummygenerator/registration/logout.html"


class SignupView(CreateView):
    template_name = "dummygenerator/registration/signup.html"
    model = UserModel
    form_class = UserCreationForm

    def form_valid(self, form):
        super().form_valid(form)
        """If the form is valid try authenticating user to skip login"""
        try:
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password1"])
            if user is not None:
                messages.success(self.request, "Profile created.")
            else:
                messages.warning(self.request, "Profile created. Error authenticating.")
                messages.warning(
                    self.request, f'{data["username"]} + {data["password1"]}',
                )

            try:
                login(self.request, user)
            except:
                raise

        except:
            messages.error(self.request, "Error authenticating.")
            raise

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        try:
            url = reverse("profile")
        except AttributeError:
            raise ImproperlyConfigured("No URL to redirect to.")
        return url


class Profile(LoginRequiredMixin, TemplateView):
    template_name = "dummygenerator/registration/profile.html"


class ListSchemas(ListView):
    pass


class EditSchemas(UpdateView):
    pass


class CreateSchemas(CreateView):
    model = FakeCSVSchema
