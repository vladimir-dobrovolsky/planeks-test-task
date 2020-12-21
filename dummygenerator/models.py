from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from faker import Faker

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
    name = models.TextField(blank=True, null=True)
    column_separator = models.CharField(
        max_length=1, choices=DELIMITER_CHOICES, default=","
    )
    string_character = models.CharField(max_length=1, choices=QUOTE_CHOCES, default='"')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f"/schemas/?{self.pk}"

    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return "Untitled schema"

    def generate_data_set(self, rows=5):
        """Method to generate dataset from schema"""
        result = {"name": self.name, "rows": rows, "content": []}
        fieldnames = self.schemacolumns.all().values()

        # import csv
        #
        # with open("some.csv", "w", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(someiterable)

        faker = Faker()

        def fake_data(data_type: int):
            faker_methods = {
                0: faker.name(),
                1: faker.job(),
                2: faker.safe_email(),
                3: faker.domain_name(),
                4: faker.phone_number(),
                5: faker.company(),
                6: faker.paragraph(nb_sentences=5, variable_nb_sentences=False),
                7: faker.random_int(0, 100),
                8: faker.address(),
                9: faker.date(),
            }
            return faker_methods[data_type]

        for i in range(1, rows + 1):
            row = []
            for name in fieldnames:
                column = name["name"]
                value = fake_data(name["data_type"])
                row.append({column: value})

            result["content"].append(row)

        return result


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
    name = models.TextField(verbose_name="column name", blank=True, null=True)
    data_type = models.IntegerField(choices=DATA_TYPES_CHOICES, verbose_name="type")
    order = models.IntegerField(blank=True, default=0)
    data_range_from = models.IntegerField(blank=True, null=True, verbose_name="from")
    data_range_to = models.IntegerField(blank=True, null=True, verbose_name="to")

    def clean(self):
        # Auto numbering columns if not entered by user
        if not self.order:
            try:
                self.order = (
                    FakeCSVSchemaColumn.objects.filter(
                        target_schema=self.target_schema
                    ).count()
                    + 1
                )
            except ObjectDoesNotExist:
                pass

    class Meta:
        ordering = ("order",)


class ExportedDataset(models.Model):
    """
    Data sets created by user
    """

    EXPORT_STATUS_CHOICES = [
        (0, "processing"),
        (1, "ready"),
        (2, "error"),
    ]
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="userdatasets"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0, choices=EXPORT_STATUS_CHOICES)
    download_link = models.URLField(null=True, blank=True)
    task_id = models.TextField()
