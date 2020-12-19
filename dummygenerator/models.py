from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.

UserModel = get_user_model()


class FakeCSVSchema(models.Model):
    """
    User-created data schemas to create datasets with fake data.
    """

    DELIMITER_CHOICES = [
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("\t", "Tab (\t)"),
        (" ", "Space ( )"),
        ("|", "Vertical bar (|)"),
    ]

    QUOTE_CHOCES = [
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')"),
    ]

    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="userschemas"
    )
    name = models.TextField()
    column_separator = models.CharField(
        max_length=1, choices=DELIMITER_CHOICES, default=","
    )
    string_character = models.CharField(max_length=1, choices=QUOTE_CHOCES, default='"')


class FakeCSVSchemaColumn(models.Model):
    """
    Columns of user-created data schemas.
    """

    DATA_TYPES_CHOICES = [
        (0, "Full name (a combination of first name and last name)"),
        (1, "Job"),
        (2, "Email"),
        (3, "Domain name"),
        (4, "Phone number"),
        (5, "Company name"),
        (6, "Text (with specified range for a number of sentences)"),
        (7, "Integer (with specified range)"),
        (8, "Address"),
        (9, "Date"),
    ]

    target_schema = models.ForeignKey(
        FakeCSVSchema, on_delete=models.CASCADE, related_name="schemacolumns"
    )
    name = models.TextField(verbose_name="column name")
    data_type = models.IntegerField(choices=DATA_TYPES_CHOICES, verbose_name="type")
    order = models.IntegerField(blank=True, default=0)

    def save(self, *args, **kwargs):
        # Auto numbering if not entered by user
        if not self.order:
            try:
                self.order = (
                    FakeCSVSchemaColumn.objects.filter(
                        target_shema=self.target_schema
                    ).count()
                    + 1
                )
            except ObjectDoesNotExist:
                pass
