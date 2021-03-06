from django import forms
from extra_views import InlineFormSet

from .models import FakeCSVSchema, FakeCSVSchemaColumn


class FakeCSVSchemaForm(forms.ModelForm):
    class Meta:
        model = FakeCSVSchema
        fields = "__all__"
        # exclude = ("author",)
        widgets = {
            "author": forms.HiddenInput(),
            "name": forms.TextInput(),
            "column_separator": forms.Select(),
            "string_character": forms.Select(),
        }


class FakeCSVSchemaColumnForm(forms.ModelForm):
    class Meta:
        model = FakeCSVSchemaColumn
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(),
            "order": forms.NumberInput(),
            "data_type": forms.Select(),
            "data_range_from": forms.NumberInput(),
            "data_range_to": forms.NumberInput(),
        }

        # TODO: conditional required attr and display logic on inputs:
        #  force required only on non-empty columns and hide range inputs
        #  from input types that don't support it

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "special", "required": True}),
        #     "order": forms.NumberInput(attrs={"class": "special"}),
        #     "data_type": forms.Select(attrs={"class": "special", "required": True}),
        #     "data_range_from": forms.NumberInput(attrs={"class": "special"}),
        #     "data_range_to": forms.NumberInput(attrs={"class": "special"}),
        # }


class FakeCSVSchemaColumnInline(InlineFormSet):
    model = FakeCSVSchemaColumn
    form_class = FakeCSVSchemaColumnForm
    fields = "__all__"

    # exclude = ("target_schema",)
    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": True,
    }


class DatasetCreateForm(forms.Form):
    rows = forms.IntegerField(label="Rows", required=True)
