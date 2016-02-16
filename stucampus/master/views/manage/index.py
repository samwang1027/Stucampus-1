#-*- coding: utf-8
import platform
import urllib
import urllib2
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator

from stucampus.custom.permission import admin_group_check
from stucampus.account.permission import check_perms

from django.conf import settings
from stucampus.utils import spec_json

from  stucampus.master.views.manage.lunarSolarConverter import LunarSolarConverter, Lunar, Solar

@login_required
def redirect(request):
    return HttpResponseRedirect('/manage/index')


@login_required
def index(request):
    return render(request, 'master/index.html')

@login_required
def send_sms(request):
    mobile = request.POST.get( 'phone' )
    name = request.POST.get( 'name' )
    response = send_bday_msg( mobile, name )
    if response['result'] == 'SUCCESS':
        return spec_json( messages='OK', status='success' )
    else:
        return spec_json( messages = response, status='errors' )



def send_bday_msg( mobile, name ):
    # 构造请求参数
    apiKey = settings.SMS_ZHIYAN_APIKEY
    appId = settings.SMS_ZHIYAN_APPID
    mobile = mobile
    templateId = settings.SMS_ZHIYAN_TPLID
    param = name
    extend =''
    uid = ''
    values = {"mobile":mobile,"param":param,"templateId":templateId,"appId":appId,"apiKey":apiKey,"extend":extend,"uid":uid}
    # 打包参数
    data = urllib.urlencode(values)
    jdata = json.dumps(values)
    url = settings.SMS_ZHIYAN_SENDURL
    # 发出请求
    req = urllib2.Request(url, jdata)
    # 接受响应内容
    response = urllib2.urlopen(req).read()
    # 处理响应内容
    response = json.loads( response )
    return response

@login_required
def convert( request ):
    year = int( request.POST.get('year') )
    month = int( request.POST.get('month') )
    day = int( request.POST.get('day') )
    leap = request.POST.get('leap', False)
    converter = LunarSolarConverter()
    lunar = Lunar( year, month, day, leap )
    solar = converter.LunarToSolar( lunar )
    return spec_json( messages=(lunar.lunarYear,lunar.lunarMonth, lunar.lunarDay), status=(solar.solarYear, solar.solarMonth, solar.solarDay) )
