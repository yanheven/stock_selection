__author__ = 'evan'
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template.loader import get_template, render_to_string

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
    return render_to_response('today/index.html', {'message': message})


def get_tomorrow(request):
    message = predict(18)
    return render_to_response('today/index.html', {'message': message})


def get_yestoday(request):
    message = predict(20)
    return render_to_response('today/index.html', {'message': message})


def test(request):
    # t = get_template('today/index.html')
    # print(t)
    # import pdb
    # pdb.set_trace()
    # # return HttpResponse(t.render())
    # return render(request, 'today/index.html')
    # try:
    #     print(render_to_string('today/templates/today/base.html'))
    #     return HttpResponse('a')
    return render_to_response('today/index.html')
    # except Exception as e:
    #     print(e)