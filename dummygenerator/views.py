from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    RedirectView,
    DetailView,
)
from django.views.generic.edit import FormMixin
from extra_views import (
    CreateWithInlinesView,
    UpdateWithInlinesView,
)

from .forms import FakeCSVSchemaForm, FakeCSVSchemaColumnInline, DatasetCreateForm
from .models import FakeCSVSchema
from .tasks import generate_csv_task

# Create your views here.

UserModel = get_user_model()


class HomeRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("home")


class HomepageView(TemplateView):
    template_name = "dummygenerator/home.html"
    # extra_context = {"page_title": "Home"}


class Login(LoginView):
    template_name = "dummygenerator/registration/login.html"
    extra_context = {"page_title": "Login"}


class Logout(LogoutView):
    template_name = "dummygenerator/registration/logout.html"


class SignupView(CreateView):
    template_name = "dummygenerator/registration/signup.html"
    model = UserModel
    form_class = UserCreationForm
    extra_context = {"page_title": "Signup"}

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
        try:
            url = reverse("profile")
        except AttributeError:
            raise ImproperlyConfigured("No URL to redirect to.")
        return url


class Profile(LoginRequiredMixin, TemplateView):
    template_name = "dummygenerator/registration/profile.html"
    extra_context = {"page_title": "Profile"}


class ListSchemas(LoginRequiredMixin, ListView):
    """
    Return the list user-created schemas.
    """

    template_name = "dummygenerator/schemas/list.html"

    def get_queryset(self):
        queryset = FakeCSVSchema.objects.filter(author=self.request.user)
        return queryset


class EditSchema(LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView):
    model = FakeCSVSchema
    form_class = FakeCSVSchemaForm
    inlines = [
        FakeCSVSchemaColumnInline,
    ]
    template_name = "dummygenerator/schemas/create.html"

    def test_func(self):
        # checking if request user is author of selected schema
        obj = self.get_object()
        if obj.author == self.request.user:
            return True

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("list")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("edit", kwargs={"pk": obj.pk})

        else:
            return reverse("list")


class CreateSchema(LoginRequiredMixin, CreateWithInlinesView):
    model = FakeCSVSchema
    form_class = FakeCSVSchemaForm
    inlines = [
        FakeCSVSchemaColumnInline,
    ]
    template_name = "dummygenerator/schemas/create.html"

    def get_initial(self):
        data = {"author": self.request.user}
        return data

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("list")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("edit", kwargs={"pk": obj.pk})

        else:
            return reverse("list")


class DeleteSchema(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FakeCSVSchema
    template_name = "dummygenerator/schemas/delete.html"

    def get_success_url(self):
        messages.success(self.request, "Deleted schema")
        return reverse("list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        # checking if request user is author of selected schema
        obj = self.get_object()
        if obj.author == self.request.user:
            return True
        else:
            return messages.error(self.request, "Error deleting schema")


class ListDataSets(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    """
    Return the list user-created schemas.
    """

    model = FakeCSVSchema
    context_object_name = "schema"
    template_name = "dummygenerator/schemas/datasets-list.html"

    form_class = DatasetCreateForm

    def test_func(self):
        # checking if request user is author of selected schema
        obj = self.get_object()
        if obj.author == self.request.user:
            return True

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        generate_csv_task.delay(
            obj=str(self.get_object().pk), rows=request.POST["rows"],
        )
        return HttpResponseRedirect(
            reverse("datasets", kwargs={"pk": self.get_object().pk})
        )
