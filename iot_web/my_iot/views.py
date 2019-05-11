from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts

from django.conf import settings

from my_iot.models import HistoryValue

def getValue():
    t = ''
    p = ''
    a = ''
    sp = ''
    if settings.CURRENT_TEMPERATURE == None:
        t = "无读数"
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_PRESSURE == None:
        p = "无读数"
    else:
        p = str(settings.CURRENT_PRESSURE)
    if settings.CURRENT_ALTITUDE == None:
        a = "无读数"
    else:
        a = str(settings.CURRENT_ALTITUDE)
    if settings.CURRENT_SEALEVELPRESSURE == None:
        sp = "无读数"
    else:
        sp = str(settings.CURRENT_SEALEVELPRESSURE)
    return t, p, a, sp

def index(request):
    t, p, a, sp = getValue()
    return render(request, 'my_iot/index.html', {'t':t, 'p':p, 'a':a, 'sp':sp})

@csrf_exempt
def communicate(request):
    if 'method' in request.GET:
        method = request.GET['method']
        data = request.GET['data']
        rts.get("http://127.0.0.1:3000/com" + "?data=" + data)
        return HttpResponse("ok")
    elif 'method' in request.POST:
        method = request.POST['method']
        data = request.POST['data']
        rts.post("http://127.0.0.1:3000/com", data={'data':data})
        return HttpResponse("ok")
    elif 'data' in request.GET:
        data = request.GET['data']
        print("I'm django received get data: " + data)
        return HttpResponse("ok")
    elif 'data' in request.POST:
        data = request.POST['data']
        print("I'm django received post data: " + data)
        return HttpResponse("ok")
    return render(request, 'my_iot/communicate.html')

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3}".format(d['t'], d['p'], d['a'], d['sp']))
        value = HistoryValue(temperature=d['t'], pressure=d['p'], altitude=d['a'], sealevelPressure=d['sp'])
        value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_PRESSURE = d['p']
        settings.CURRENT_ALTITUDE = d['a']
        settings.CURRENT_SEALEVELPRESSURE = d['sp']
    if 'get' in request.GET:
        rts.get("http://192.168.137.32:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        t, p, a, sp = getValue()
        return HttpResponse(json.dumps({'t':t, 'p':p, 'a':a, 'sp':sp}))
    return HttpResponse("ok")