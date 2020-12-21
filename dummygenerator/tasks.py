from time import sleep

from celery import shared_task
from django.contrib.auth import get_user_model

from .models import FakeCSVSchema, ExportedDataset

UserModel = get_user_model()


@shared_task
def generate_csv_task(obj=None, author=None, rows=None):
    author = UserModel.objects.get(pk=author)
    schema = FakeCSVSchema.objects.get(pk=int(obj))
    dataset = ExportedDataset()
    if schema.generate_data_set(rows=int(rows)):
        sleep(60)
        return True

    return False
