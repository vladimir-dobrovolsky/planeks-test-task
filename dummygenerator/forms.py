from django import forms
from .models import FakeCSVSchema, FakeCSVSchemaColumn
from extra_views import InlineFormSetFactory, InlineFormSet


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
    rows = forms.IntegerField(label="Rows")
