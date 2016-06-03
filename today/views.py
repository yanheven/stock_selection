# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template.loader import get_template, render_to_string

from today_trade import predict, report, get_predict_message
from today_trade import get_predict_message_399006, predict_399006, report_399006
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
    message = get_predict_message()
    return render_to_response('today/index.html', {'message': message})


def get_talbe(request):
    message = predict()
    context = dict(date=message[0].split()[0],
                   time=message[0],
                   data_1=message[1],
                   data_2=message[2],
                   data_20_1=message[3],
                   data_20_2=message[4],
                   chg_1=message[5],
                   chg_2=message[6],
                   signal=message[7],
                   date_20=message[8])
    return render_to_response('today/table.html', context)


def get_tomorrow(request):
    message = get_predict_message(18)
    return render_to_response('today/index.html', {'message': message})


def get_yestoday(request):
    message = get_predict_message(20)
    return render_to_response('today/index.html', {'message': message})


def get_report(request):
    message = report().replace('\n', '</br>')
    return HttpResponse(message)


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


def get_399006(request):
    message = predict_399006()
    context = dict(date=message[0].split()[0],
                   time=message[0],
                   data=message[1],
                   data_20=message[2],
                   chg=message[3],
                   signal=message[4],
                   date_20=message[5])
    return render_to_response('today/399006.html', context)


def get_399006_origin(request):
    message = get_predict_message_399006()
    return render_to_response('today/index.html', {'message': message})


def get_399006_report(request):
    message = report_399006().replace('\n', '</br>')
    return HttpResponse(message)