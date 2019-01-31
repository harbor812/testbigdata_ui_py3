from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render,render_to_response
import json
from django.template import RequestContext
from django import forms
from tcrl import models
from dwebsocket.decorators import accept_websocket,require_websocket
import paramiko
import datetime,time
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# Create your views here.
from django.views.decorators.cache import cache_page



#API 接口
# class GetMessageView(APIView):
#     # get 请求
#     def get(self, request):
#         # 获取参数数据
#         get = request.GET
#         # 获取参数 a
#         a = get.get('a')
#         print(a)
#         # 返回信息
#         d = {
#             'status': 1,
#             'message': a,
#             }
#         return JsonResponse(d)
#     def post(self, request):
#         # 获取参数数据
#         get = request.POST
#         # 获取参数 a
#         a = get.get('a')
#         print(a)
#         # 返回信息
#         d = {
#             'status': 1,
#             'message': a,
#             }
#         return JsonResponse(d)

def getcommentdetail(request):
    if request.method=='GET':
        changename=request.GET.get('changename')
        object_id = request.GET.get('object_id')
        comment = request.GET.get('comment')
    if request.method == 'POST':
        changename=request.POST.get('changename')
        object_id = request.POST.get('object_id')
        comment = request.POST.get('comment')
    if changename !='' and object_id !='' and comment !='':
        sql='changename like \'%'+ changename +'%\' and object_id ='+ object_id +' and  comment= \''+ comment + '\''
        com_detail=models.bug.objects.changename_comment_sel(sql)
        # print("############,"+com_detail)
        if com_detail !=None:
            json_code={'if_cn':com_detail[0],'for_cn':com_detail[1],'switch_cn':com_detail[2],'while_cn':com_detail[3]}
        else:
            json_code={'message':0}
    else:
        json_code = {'error': 'Filed can not null'}
    return JsonResponse(json_code)
#登录页
def login(request):
    print("进入:",request)
    error_message=""
    if request.method == 'POST':
        print("调 POST")
        #获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        print (username,password)
        #与数据库比对
        user = models.User.objects.filter(username__exact=username, password__exact=password)
        if user:
            # 比对通过，跳转index
            response = HttpResponseRedirect('/index/')
            #写cookie，失效时间：3600秒
            response.set_cookie('username', username, 3600)
            return response

        else:
            print("进入 login")
           # return HttpResponseRedirect('/login/ ')
            error_message='用户名或密码错误,请重新登录'
    print (error_message)
    return render_to_response('login.html',{'error_message':error_message})

#登录成功进入主页
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):
     username=request.COOKIES.get('username','')
     if username:
         print("进入 index def:",username)
         userdata=models.User.objects.filter(username__contains=username)
         for row in userdata:
             username=row.nickname
             print (username)
         newbugcount=models.bug.objects.bug_count('新建')
         closebugcount = models.bug.objects.bug_count('完成')
         jenkinscount = models.bug.objects.jenkins_count()
         newbug7count=models.bug.objects.bug_7count('新建')
         # closebug7count = models.bug.objects.bug_7count('完成')
         bugtagl30count=models.bug.objects.bugtagl30_count()
         jenkins7count = models.bug.objects.jenkins_7count()
         buglevel30count = models.bug.objects.buglevel30_count()
         onlinebug30count= models.bug.objects.onlinebug30_count()
         return render_to_response('index.html',
                                   {'username':username,
                                    'newbugcount':newbugcount,
                                    'closebugcount':closebugcount,
                                    'jenkinscount':jenkinscount,
                                    'newbug7count':json.dumps(newbug7count,separators=(',',':')),
                                    'bugtagl30count':json.dumps(bugtagl30count,separators=(',',':')),
                                    'buglevel30count': json.dumps(buglevel30count, separators=(',', ':')),
                                    'onlinebug30count': onlinebug30count,
                                    'jenkins7count':json.dumps(jenkins7count,separators=(',',':'))
                                    })
     else:
         response = HttpResponseRedirect('/login/')
         return response
#登出，并清理cookie
def logout(request):
     print("logout")
     response=HttpResponseRedirect('/login/')
     response.delete_cookie('username')
     return response
#进入泡面番基础数据分析页:table_basic
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def paomianfan_data(request):
     username=request.COOKIES.get('username','')
     if username:
         print("进入 paomianfan_data:",username)
         userdata=models.User.objects.filter(username__contains=username)
         for row in userdata:
             username=row.nickname
             print (username)
         fenciqian_30count_list=models.bug.objects.fenci_30count('1')
         fencihou_30count_list = models.bug.objects.fenci_30count('2')
         fenciios_30count_list=models.bug.objects.fenci_30count('16')
         fenciandrodd_30count_list = models.bug.objects.fenci_30count('25')
         fencifan_30count_list = models.bug.objects.fenci_30count('21')
         fencifanios_30count_list = models.bug.objects.fenci_30count('22')
         fencifanandrodd_30count_list = models.bug.objects.fenci_30count('22')
         fencitongxingzheng_30count_list = models.bug.objects.fenci_30count('4')
         tool_30count_list = models.bug.objects.fenci_30count('12')
         fencicommitcodeqian_30count_list = models.bug.objects.fencicommitcode_30count('1')
         fencicommitcodehou_30count_list = models.bug.objects.fencicommitcode_30count('2')
         fencicommitcodefan_30count_list = models.bug.objects.fencicommitcode_30count('21')
         fencicommitcodetongxingzheng_30count_list = models.bug.objects.fencicommitcode_30count('4')
         qiancommitcode_buglist = models.bug.objects.commitcode_bug('1')
         houcommitcode_buglist = models.bug.objects.commitcode_bug('2')
         fancommitcode_buglist = models.bug.objects.commitcode_bug('21')
         tongxingzhengcommitcode_buglist = models.bug.objects.commitcode_bug('4')

         fencifanqianbao_30count_list = models.bug.objects.fenci_30count('18')
         fencicommitcodefanqianbao_30count_list = models.bug.objects.fencicommitcode_30count('18')
         fanqianbaocommitcode_buglist = models.bug.objects.commitcode_bug('18')

         fencixqgame_30count_list = models.bug.objects.fenci_30count('24')
         fencicommitcodexqgame_30count_list = models.bug.objects.fencicommitcode_30count('24')
         xqgamecommitcode_buglist = models.bug.objects.commitcode_bug('24')

         return render_to_response('paomianfan_fenxi.html',{'username':username,
                                                       'fencixqgame_30count_list': fencixqgame_30count_list,
                                                       'fencicommitcodexqgame_30count_list': fencicommitcodexqgame_30count_list,
                                                       'xqgamecommitcode_buglist': xqgamecommitcode_buglist,
                                                       'fencifanqianbao_30count_list': fencifanqianbao_30count_list,
                                                       'fencicommitcodefanqianbao_30count_list': fencicommitcodefanqianbao_30count_list,
                                                       'fanqianbaocommitcode_buglist': fanqianbaocommitcode_buglist,
                                                       'fencitongxingzheng_30count_list': fencitongxingzheng_30count_list,
                                                       'fencicommitcodetongxingzheng_30count_list': fencicommitcodetongxingzheng_30count_list,
                                                       'tongxingzhengcommitcode_buglist': tongxingzhengcommitcode_buglist,
                                                       'fenciqian_30count_list':fenciqian_30count_list,
                                                       'fencihou_30count_list':fencihou_30count_list,
                                                       'fencicommitcodefan_30count_list': fencicommitcodefan_30count_list,
                                                       'fencicommitcodeqian_30count_list':fencicommitcodeqian_30count_list,
                                                       'fencicommitcodehou_30count_list':fencicommitcodehou_30count_list,
                                                       'fancommitcode_buglist': fancommitcode_buglist,
                                                       'qiancommitcode_buglist': qiancommitcode_buglist,
                                                       'houcommitcode_buglist': houcommitcode_buglist,
                                                       'fenciios_30count_list': fenciios_30count_list,
                                                       'fenciandrodd__30count_list': fenciandrodd_30count_list,
                                                       'tool_30count_list': tool_30count_list,
                                                       'fencifan_30count_list': fencifan_30count_list,
                                                       'fencifanios_30count_list': fencifanios_30count_list,
                                                       'fencifanandrodd_30count_list': fencifanandrodd_30count_list
                                                       })
     else:
         response = HttpResponseRedirect('/login/')
         return response
#进入大数据分析基础数据分析页
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def bigdata_data(request):
         username = request.COOKIES.get('username', '')
         if username:
             print("进入 paomianfan_data:", username)
             userdata = models.User.objects.filter(username__contains=username)
             for row in userdata:
                 username = row.nickname
                 print(username)
             fenciqian_30count_list = models.bug.objects.fenci_30count('1')
             fencihou_30count_list = models.bug.objects.fenci_30count('2')
             fenciios_30count_list = models.bug.objects.fenci_30count('16')
             fenciandrodd_30count_list = models.bug.objects.fenci_30count('15')
             fencicommitcodeqian_30count_list = models.bug.objects.fencicommitcode_30count('1')
             fencicommitcodehou_30count_list = models.bug.objects.fencicommitcode_30count('2')
             qiancommitcode_buglist = models.bug.objects.commitcode_bug('1')
             houcommitcode_buglist = models.bug.objects.commitcode_bug('2')
             objectname_list=models.bug.objects.serch_object_name()
             print("objectname:",objectname_list)
             return render_to_response('table_basic_bigdata.html', {'username': username,
                                                            'fenciqian_30count_list': fenciqian_30count_list,
                                                            'fencihou_30count_list': fencihou_30count_list,
                                                            'fencicommitcodeqian_30count_list': fencicommitcodeqian_30count_list,
                                                            'fencicommitcodehou_30count_list': fencicommitcodehou_30count_list,
                                                            'qiancommitcode_buglist': qiancommitcode_buglist,
                                                            'houcommitcode_buglist': houcommitcode_buglist,
                                                            'fenciios_30count_list': fenciios_30count_list,
                                                            'fenciandrodd_30count_list': fenciandrodd_30count_list,
                                                            'objectname_list': objectname_list
                                                            })
         else:
             response = HttpResponseRedirect('/login/')
             return response
# 进入其他项目基础数据分析页
def other_data(request):
             username = request.COOKIES.get('username', '')
             if username:
                 print("进入 paomianfan_data:", username)
                 userdata = models.User.objects.filter(username__contains=username)
                 for row in userdata:
                     username = row.nickname
                     print(username)
                 fenciqian_30count_list = models.bug.objects.fenci_30count('1')
                 fencihou_30count_list = models.bug.objects.fenci_30count('2')
                 fenciios_30count_list = models.bug.objects.fenci_30count('16')
                 fenciandrodd_30count_list = models.bug.objects.fenci_30count('15')
                 fencifan_30count_list = models.bug.objects.fenci_30count('18')
                 fencifanios_30count_list = models.bug.objects.fenci_30count('19')
                 fencifanandrodd_30count_list = models.bug.objects.fenci_30count('20')
                 fencicommitcodeqian_30count_list = models.bug.objects.fencicommitcode_30count('1')
                 fencicommitcodehou_30count_list = models.bug.objects.fencicommitcode_30count('2')
                 qiancommitcode_buglist = models.bug.objects.commitcode_bug('1')
                 houcommitcode_buglist = models.bug.objects.commitcode_bug('2')

                 return render_to_response('table_basic_other.html', {'username': username,
                                                                'fenciqian_30count_list': fenciqian_30count_list,
                                                                'fencihou_30count_list': fencihou_30count_list,
                                                                'fencicommitcodeqian_30count_list': fencicommitcodeqian_30count_list,
                                                                'fencicommitcodehou_30count_list': fencicommitcodehou_30count_list,
                                                                'qiancommitcode_buglist': qiancommitcode_buglist,
                                                                'houcommitcode_buglist': houcommitcode_buglist,
                                                                'fenciios_30count_list': fenciios_30count_list,
                                                                'fenciandrodd_30count_list': fenciandrodd_30count_list,
                                                                'fencifan_30count_list': fencifan_30count_list,
                                                                'fencifanios_30count_list': fencifanios_30count_list,
                                                                'fencifanandrodd_30count_list': fencifanandrodd_30count_list
                                                                })
             else:
                 response = HttpResponseRedirect('/login/')
                 return response
#进入bug查询列表
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def bug_detail(request,page,page1):
    username = request.COOKIES.get('username', '')
    if username:
        print("进入 bug_detail:", username)
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
            bug_count_list = models.bug.objects.bug_detail(page,page1)
        return render_to_response('table_advanced.html',{'username':username,
                                                         'bug_count_list': bug_count_list}
                                  )
    else:
        response = HttpResponseRedirect('/login/')
        return response
# 进入bug查询列表more
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def bugmore_detail(request, page,page1):
        username = request.COOKIES.get('username', '')
        if username:
            print("进入 bug_detail:", username)
            userdata = models.User.objects.filter(username__contains=username)
            for row in userdata:
                username = row.nickname
                print(page1)
                page1=int(page1)
                if page1 == 1:
                    print(page1)
                    page1= " and is_miss=1"
                else:
                    page1=''
                bug_count_list = models.bug.objects.bugmore_detail(page,page1)
            return render_to_response('table_advanced.html', {'username': username,
                                                              'bug_count_list': bug_count_list }
                                      )
        else:
            response = HttpResponseRedirect('/login/')
            return response

# @cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
# def bugmissmore_detail(request, page, page1):
#             username = request.COOKIES.get('username', '')
#             if username:
#                 print("进入 bug_detail:", username)
#                 userdata = models.User.objects.filter(username__contains=username)
#                 for row in userdata:
#                     username = row.nickname
#                     print(page1)
#                     page1 = int(page1)
#                     if page1 == 1:
#                         print(page1)
#                         page1 = " and is_miss=1"
#                     else:
#                         page1 = ''
#                     bug_count_list = models.bug.objects.bugmore_detail(page, page1)
#                 return render_to_response('table_bugmiss.html', {'username': username,
#                                                                   'bug_count_list': bug_count_list}
#                                           )
#             else:
#                 response = HttpResponseRedirect('/login/')
#                 return response
# 进入bug查询列表
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def bugname_detail(request, page, page1,page2):
    username = request.COOKIES.get('username', '')
    if username:
        print("进入 bug_detail:", username)
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
            page = "bug_name like '%" + page + "%'"
            bugname_count_list = models.bug.objects.bugname_detail(page,page1,page2)
        return render_to_response('table_advanced.html', {'username': username,
                                                          'bug_count_list': bugname_count_list}
                                  )
    else:
        response = HttpResponseRedirect('/login/')
        return response
#进入jenkins查询列表 commitcode
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def jenkins_detail(request, page):
        username = request.COOKIES.get('username', '')
        if username:
            print("进入 jenkins_detail:", username)
            userdata = models.User.objects.filter(username__contains=username)
            for row in userdata:
                username = row.nickname
                page=page.replace(',','","')
                page='"'+page+'"'
                jenkins_count_list = models.bug.objects.jenkins_detail(page)
            return render_to_response('table_jenkins.html', {'username': username,
                                                              'jenkins_count_list': jenkins_count_list }
                                      )
        else:
            response = HttpResponseRedirect('/login/')
            return response
# 进入jenkins查询列表 changge_name
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def jenkins1_detail(request, page):
            username = request.COOKIES.get('username', '')
            if username:
                print("进入 jenkins1_detail:", username)
                userdata = models.User.objects.filter(username__contains=username)
                for row in userdata:
                    username = row.nickname
                    page = page.replace(',', '","')
                    page = '"' + page + '"'
                    jenkins_count_list = models.bug.objects.jenkins1_detail(page)
                return render_to_response('table_jenkins.html', {'username': username,
                                                                 'jenkins_count_list': jenkins_count_list }
                                          )
            else:
                response = HttpResponseRedirect('/login/')
                return response
# 进入jenkins查询列表 more
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def jenkinsmore_detail(request):
            username = request.COOKIES.get('username', '')
            if username:
                print("进入 jenkins1_detail:", username)
                userdata = models.User.objects.filter(username__contains=username)
                for row in userdata:
                    username = row.nickname
                    jenkins_count_list = models.bug.objects.jenkinsmore_detail()
                return render_to_response('table_jenkins.html', {'username': username,
                                                                 'jenkins_count_list': jenkins_count_list }
                                          )
            else:
                response = HttpResponseRedirect('/login/')
                return response

# 进入代码 问题分析查询列表
def changename_analyze(request,page):
                username = request.COOKIES.get('username', '')
                if username:
                    print("changename_analyze:", username)
                    userdata = models.User.objects.filter(username__contains=username)
                    for row in userdata:
                        username = row.nickname
                        if page != 'all':
                            name ="and  js.change_name=" + '"'+page+'"'
                            changename_analyze_list = models.bug.objects.changename_analyze(name)
                        else:
                            changename_analyze_list = models.bug.objects.changename_analyze("")
                    return render_to_response('changename_analyze.html', {'username': username,
                                                                     'changename_analyze_list': changename_analyze_list}
                                              )
                else:
                    response = HttpResponseRedirect('/login/')
                    return response
# 进入每日查询列表（暂时废弃）
def day_detail(request):
            username = request.COOKIES.get('username', '')
            if username:
                print("进入 day_detail:", username)
                userdata = models.User.objects.filter(username__contains=username)
                for row in userdata:
                    username = row.nickname
                    day_statistics_7detail_list = models.bug.objects.day_statistics_7detail()
                return render_to_response('table_daydata.html', {'username': username,
                                                                 'day_statistics_7detail_list': day_statistics_7detail_list }
                                          )
            else:
                response = HttpResponseRedirect('/login/')
                return response
#每日数据查询
def day_search(request):
    print("进入:",request)
    username = request.COOKIES.get('username', '')
    day_statistics_detail_list=''
    objectname_list=''
    if username:
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
            objectname_list = models.bug.objects.search_object_name()
            # print ("objectname_list:", objectname_list)
        if request.method == 'POST':
            print("调 POST")
            date_ff="day_statistics.date >='1700-00-00' and "
            date_tt = " day_statistics.date <='2099-12-31' and "
            object_nn=" day_statistics.object_id in (select object_id from object_name)"
            #获取用户名和密码
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            object_name = request.POST.get('object_name')
            if date_from:
                date_ff="day_statistics.date >='"+date_from+"' and "
            if date_to:
                date_tt=" day_statistics.date <='"+date_to+"' and "
            if object_name:
                object_nn=" day_statistics.object_id='"+object_name+"'"
            sql=date_ff+date_tt+object_nn
            # print ("sql:", sql)
            day_statistics_detail_list = models.bug.objects.day_statistics_search_detail(sql)
            # print ("day_statistics_detail_list:", day_statistics_detail_list)
        return render_to_response('table_daydata_search.html', {'username': username,
                                                             'day_statistics_detail_list': day_statistics_detail_list,
                                                             'objectname_list': objectname_list
                                                                }
                                      )
    else:
        response = HttpResponseRedirect('/login/')
        return response
#jenkins数据查询
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def jenkins_search(request):
    print("进入:",request)
    username = request.COOKIES.get('username', '')
    jenkins_search_detail_list=''
    objectname_list=''
    if username:
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
            objectname_list = models.bug.objects.search_object_name()

        if request.method == 'POST':
            print("调 POST")
            commitcodec=""
            change_namec=""
            date_ff="jenkins_source.date >='1700-00-00' and "
            date_tt = " jenkins_source.date <='2099-12-31' and "
            object_nn=" jenkins_source.object_id in (select object_id from object_name)"
            # 获取数据
            commitcode = request.POST.get('commitcode')
            change_name = request.POST.get('change_name')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            object_name = request.POST.get('object_name')
            if commitcode:
                commitcodec="jenkins_source.commitcode like '%"+commitcode+"%' and "
            if change_name:
                change_namec="jenkins_source.change_name like '%"+change_name+"%' and "
            if date_from:
                date_ff="jenkins_source.date >='"+date_from+"' and "
            if date_to:
                date_tt=" jenkins_source.date <='"+date_to+"' and "
            if object_name:
                object_nn=" jenkins_source.object_id='"+object_name+"'"
            sql=commitcodec + change_namec + date_ff + date_tt + object_nn
            # print ("sql:", sql)
            jenkins_search_detail_list = models.bug.objects.jenkins_search_detail(sql)
            # print ("jenkins_search_detail_list:", jenkins_search_detail_list)
        return render_to_response('table_jenkins_search.html', {'username': username,
                                                                'jenkins_search_detail_list': jenkins_search_detail_list,
                                                                'objectname_list':objectname_list}
                                      )
    else:
        response = HttpResponseRedirect('/login/')
        return response
#bug 查询
@cache_page(60 * 10)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def bug_search(request):
        print("进入:", request)
        username = request.COOKIES.get('username', '')
        bug_search_detail_list = ''
        objectname_list=''
        if username:
            userdata = models.User.objects.filter(username__contains=username)
            for row in userdata:
                username = row.nickname
                objectname_list = models.bug.objects.search_object_name()
            if request.method == 'POST':
                print("调 POST")
                bug_idd=""
                bug_namen=""
                status_s=" bug.bug_status in ('新建','已提交','完成') and "
                date_ff = "bug.date >='1700-00-00' and "
                date_tt = " bug.date <='2099-12-31' and "
                main_object_nn = " bug.type in ('泡面番','大数据系统','区块链开发团队','应用中心系统') and "
                object_nn = " bug.sub_type in (select object_id from object_name) and "
                is_miss_nn = " bug.is_miss in (0,1)"
                buglevel_nn = ""
                # 获取数据
                bug_id = request.POST.get('bug_id')
                bug_name = request.POST.get('bug_name')
                status = request.POST.get('status')
                date_from = request.POST.get('date_from')
                date_to = request.POST.get('date_to')
                main_object_name = request.POST.get('main_object_name')
                object_name = request.POST.get('object_name')
                is_miss = request.POST.get('is_miss_status')
                bug_level = request.POST.get('bug_level')
                if bug_id:
                    bug_idd = "bug.bug_id='" + bug_id + "' and "
                if bug_name:
                    bug_namen = "bug.bug_name like '%" + bug_name + "%' and "
                if status:
                    status_s = "bug.bug_status ='" + status + "' and "
                if date_from:
                    date_ff = "bug.date >='" + date_from + "' and "
                if date_to:
                    date_tt = " bug.date <='" + date_to + "' and "
                if main_object_name:
                    main_object_nn = " bug.type='" + main_object_name + "' and "
                if object_name:
                    object_nn = " bug.sub_type='" + object_name + "' and "
                if is_miss:
                    is_miss_nn = " bug.is_miss='" + is_miss + "'"
                if bug_level:
                    if bug_level =='4':
                        buglevel_nn = " bug.level_id is null and "
                    else:
                        buglevel_nn = " bug.level_id='" + bug_level + "' and "
                sql = bug_idd + bug_namen + status_s + date_ff + date_tt + main_object_nn + object_nn + buglevel_nn + is_miss_nn
                print("sql:", sql)
                bug_search_detail_list = models.bug.objects.bug_search_detail(sql)
                # print("bug_search_detail_list:", bug_search_detail_list)
            return render_to_response('table_bug_search.html', {'username': username,
                                                                'bug_search_detail_list': bug_search_detail_list,
                                                                'objectname_list':objectname_list}
                                      )
        else:
            response = HttpResponseRedirect('/login/')
            return response

######################################################################################

def chat33(request):
    return render(request, 'message.html')

def exec_command(comm):
    starttime = datetime.datetime.now()
    print (comm,starttime)
    rs=[]
    username = 'qa'
    password = 'QAadmin@123'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('113.107.166.5',19116,username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.readlines()
    ssh.close()
    # print ("###########查询结果######################")
    # print (result)
    for i in range(len(result)):
        if '严重的程序' in result[i]:
            rs1=result[i].split("INFO")
            rs.append(rs1[1].strip())
            # rs.append(result[i])
    print (rs)
    result=str(rs)
    result=result.replace('\\n','').replace('[','').replace(']','').replace('\\x00','')
    result = result.replace('\',', '\'\n').encode('utf-8').strip()
    return result


@require_websocket
def echo_once1(request):
    # print('###########################################')
    # print (request.is_websocket())
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'message.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')
            if message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                starttime=datetime.datetime.now()
                date=str(datetime.date.today())+' 23:00:00'
                endtime=datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
                command = 'cat /python/nohup.out'#这里是要执行的命令或者脚本
                # print ('###########################################')
                print (exec_command(command))
                jg=""
                jg1=""
                while starttime < endtime and request.websocket:
                     jg=exec_command(command)
                     if jg != jg1:
                          request.websocket.send(jg)  # 发送消息到客户端
                     #    request.websocket.send("test")
                          jg1=jg
                     time.sleep(30)
                     starttime = datetime.datetime.now()
            else:
                request.websocket.send('没权限!!!'.encode('utf-8'))