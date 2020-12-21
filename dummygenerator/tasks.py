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
def generate_csv_task(self, obj=None, author=None, rows=None):
    logger.info(f"=======================")
    logger.info(f"request: {self.request.id}")
    logger.info(f"=======================")
    author = UserModel.objects.get(pk=author)
    schema = FakeCSVSchema.objects.get(pk=int(obj))
    request_id = self.request.id
    dataset = ExportedDataset()
    if schema.generate_data_set(rows=int(rows)):
        sleep(15)
        return True

    return False
