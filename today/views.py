__author__ = 'evan'
from django.http import HttpResponse

from today_trade import predict


def get(request):
    message = predict()
    return HttpResponse(message)


def get_tomorrow(request):
    message = predict(18)
    return HttpResponse(message)


def get_yestoday(request):
    message = predict(20)
    return HttpResponse(message)
