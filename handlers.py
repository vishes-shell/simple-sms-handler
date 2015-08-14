import requests
import json
from django.db import models


class SmsHandlerLog(models.Model):
    """
    Description:
        Logs of sms handlers
    """
    class Meta:
        db_table = 'sms_handler_log'
        verbose_name = 'handler log'
        verbose_name_plural = 'handler logs'

    handler_name = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)
    phone = models.CharField(max_length=14)
    error_code = models.SmallIntegerField(blank=True)
    error_msg = models.CharField(max_length=100, blank=True)


class Handler(object):
    def __init__(self, url):
        self.url = url

    def send(self, user_data):
        response = json.loads(requests.post(self.url, data=user_data))
        status = response['status']
        handler_log = SmsHandlerLog(handler_name=self.__class__.__name__, status=status, phone=response['phone'])
        if status == 'error':
            handler_log.error_code = response['error_code']
            handler_log.error_msg = response['error_msg']
        handler_log.save()


class HandlerCenter(Handler):
    pass

class HandlerTraffic(Handler):
    pass

def get_handler(handler_name):
    for sbcls in Handler.__subclasses__():
        if type(sbcls).__name__ == handler_name:
            return sbcls

HandlerCenter('http://smsc.ru/some­api/message/')
HandlerTraffic('http://smstraffic.ru/super­api/message/')
