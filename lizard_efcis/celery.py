from __future__ import absolute_import

from celery import Celery

from django.conf import settings

app = Celery('lizard_efcis')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    #BROKER_URL='amqp://rabbitmq:7QqBANc@119-rmq-d1.external-nens.local:5672/efcis',
    CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler',
    CELERY_IMPORTS=("lizard_efcis.tasks", ),
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
