from __future__ import absolute_import

from celery import Celery

# set the default Django settings module for the 'celery' program.

from django.conf import settings

app = Celery('lizard_efcis')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    BROKER_URL='django://',
    CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler',
    CELERY_IMPORTS=("lizard_efcis.tasks", ),
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
