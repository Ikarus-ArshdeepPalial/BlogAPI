from celery import shared_task

@shared_task
def compute_summary_task():
    return "Done"

@shared_task
def compute_category_task():
    return "Done"