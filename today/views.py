__author__ = 'evan'
from django.http import HttpResponse

from today_trade import predict
import logger


LOG = logger.get_loger()


def log_ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    path = request.get_full_path()
    LOG.warn(ip + path)

def get(request):
    message = predict()
    return HttpResponse(message)


def get_tomorrow(request):
    message = predict(18)
    return HttpResponse(message)


def get_yestoday(request):
    message = predict(20)
    return HttpResponse(message)


def test(request):
    return HttpResponse('<h1>test</h1>')
