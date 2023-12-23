from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
import traceback
from metar import settings
import time
from . import redis_cache
import json
import logging


STATION_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"
redis_conn = None

def redis_connection():

    """ redis connection stablishing """

    global redis_conn
    if redis_conn:
        return redis_conn
    try:
        print("redist connecting")
        redis_conn = redis_cache.BaseCache(**settings.REDIS_CACHE_DB)
    except Exception as e:
        print("Exception while redis_connection {}".format(e))
    return redis_conn

def read_data(scode):

    """ reading weather condition using station code """

    try:
        logging.info("RAJU testing loging")
        print("Inside read_data: ", scode)
        json_data = {}
        from urllib.request import urlopen
        station_url = STATION_URL + scode + '.TXT'
        file  = urlopen(station_url)
        data = file.read().decode('utf8')
        data = data.split('\n')
        json_data['last_observation'] = data[0].split(' ')[0] + 'At' + data[0].split(' ')[1] + 'GMT'
        json_data['station'] = scode
        json_data['miscellaneous_data'] = data[1]
        print("data read succeeed")
    except Exception as e:
        return JsonResponse({"Exception While URL Open": e}, status=status.HTTP_400_BAD_REQUEST)
    return json.dumps(json_data)

def status(request):
    if request.method == 'POST':
        tmp = 'xyz'
        return JsonResponse({"status ping": tmp})
    else:
        pass



@api_view(['GET'])
def redis_details(request):

    if request.method == 'GET':
        print("raju 1")
        redis_conn = redis_connection()
        if redis_conn:
            keys = redis_conn.keys(pattern='*')
            print(type(keys))
            dict_d = {}
            for key in keys:
                # redis_conn.get(key)
                print("before deicoding: ", type(key))
                key = key.decode("utf8")
                print(type(key))
                dict_d[key] = redis_conn.get(key)

            # data = json.dumps(dict_d)
            # dict_d = {}
            return  JsonResponse({'data': str(dict_d)})
        else:
            print("redis connection failed")


@api_view(['GET'])
def weather_status(request):

    """ API to read weather condition """

    if request.method == 'GET':
        scode = request.GET.get('scode', None)
        nocache = request.GET.get('nocache', None)
        redis_conn = redis_connection()
        if redis_conn:
            if nocache == '1':
                print("Updating live data into cache")
                data = read_data(scode)   ## read live data for scode
                redis_conn.delete(scode)   ## delete existing code with metar data
                redis_conn.set(scode, data, 60*5)    ##cache redis with data and expiry time as 5 minute
            elif not redis_conn.get(scode):
                print("Cache missed")
                data = read_data(scode)  ## read data for scode
                redis_conn.set(scode, data, 60*5)
            else:
                print("Cache hit success")
                data = redis_conn.get(scode).decode("utf8")  ## read data from redis
        return JsonResponse({'data': str(data)})
    else:
        pass

@api_view(['GET'])
def ping(request):

    """simple ping pong test"""

    return JsonResponse({'data': 'pong'})
