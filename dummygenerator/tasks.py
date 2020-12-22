from time import sleep

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from .models import FakeCSVSchema, ExportedDataset

UserModel = get_user_model()
logger = get_task_logger(__name__)


# task.AsyncResult(task.request.id).state
# to check state


@shared_task(bind=True)
def generate_csv_task(self, obj=None, rows=None):
    schema = FakeCSVSchema.objects.get(pk=int(obj))
    task_id = self.request.id

    # creating dataset entry
    dataset = ExportedDataset(schema=schema, task_id=task_id, status=0)
    dataset.save()
    try:
        # generating dataset csv file and storing its url
        result = schema.generate_data_set(rows=int(rows), uid=task_id)
        if result:
            dataset.download_link = result
            dataset.status = 1
            dataset.save()
        return True

    except:
        # setting dataset status = error
        dataset.status = 2
        dataset.save()
        raise
