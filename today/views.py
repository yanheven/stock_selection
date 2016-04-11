__author__ = 'evan'
from django.http import HttpResponse

from today_trade import predict

def get(request):
    message = predict()
    return HttpResponse(message)