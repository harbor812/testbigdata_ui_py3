from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,render_to_response
import json
from django.template import RequestContext
from django import forms
from tcrl import models
# Create your views here.


def add(request):
    if request.mothod == 'POST':
        a = request.POST.get['a']
        b = request.POST.get['b']
        c = {'结果':int(a)+int(b)}
        print (c)
        return HttpResponse(json.dump(c))
    if request.mothod == 'GET':
        return HttpResponse("OK")

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
         closebug7count = models.bug.objects.bug_7count('完成')
         jenkins7count = models.bug.objects.jenkins_7count()
         return render_to_response('index.html',
                                   {'username':username,'newbugcount':newbugcount,'closebugcount':closebugcount,'jenkinscount':jenkinscount,'newbug7count':json.dumps(newbug7count,separators=(',',':')),'closebug7count':json.dumps(closebug7count,separators=(',',':')),'jenkins7count':json.dumps(jenkins7count,separators=(',',':'))})
     else:
         response = HttpResponseRedirect('/login/')
         return response
#登出，并清理cookie
def logout(request):
     print("logout")
     response=HttpResponseRedirect('/login/')
     response.delete_cookie('username')
     return response
#进入泡面番基础数据分析页
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
         fenciandrodd_30count_list = models.bug.objects.fenci_30count('15')
         fencicommitcodeqian_30count_list = models.bug.objects.fencicommitcode_30count('1')
         fencicommitcodehou_30count_list = models.bug.objects.fencicommitcode_30count('2')
         qiancommitcode_buglist = models.bug.objects.commitcode_bug('1')
         houcommitcode_buglist = models.bug.objects.commitcode_bug('2')

         return render_to_response('table_basic.html',{'username':username,
                                                       'fenciqian_30count_list':fenciqian_30count_list,
                                                       'fencihou_30count_list':fencihou_30count_list,
                                                       'fencicommitcodeqian_30count_list':fencicommitcodeqian_30count_list,
                                                       'fencicommitcodehou_30count_list':fencicommitcodehou_30count_list,
                                                       'qiancommitcode_buglist': qiancommitcode_buglist,
                                                       'houcommitcode_buglist': houcommitcode_buglist,
                                                       'fenciios_30count_list': fenciios_30count_list,
                                                       'fenciandrodd_30count_list': fenciandrodd_30count_list
                                                       })
     else:
         response = HttpResponseRedirect('/login/')
         return response
#进入大数据分析基础数据分析页
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

             return render_to_response('table_basic_bigdata.html', {'username': username,
                                                            'fenciqian_30count_list': fenciqian_30count_list,
                                                            'fencihou_30count_list': fencihou_30count_list,
                                                            'fencicommitcodeqian_30count_list': fencicommitcodeqian_30count_list,
                                                            'fencicommitcodehou_30count_list': fencicommitcodehou_30count_list,
                                                            'qiancommitcode_buglist': qiancommitcode_buglist,
                                                            'houcommitcode_buglist': houcommitcode_buglist,
                                                            'fenciios_30count_list': fenciios_30count_list,
                                                            'fenciandrodd_30count_list': fenciandrodd_30count_list
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
                                                                'fenciandrodd_30count_list': fenciandrodd_30count_list
                                                                })
             else:
                 response = HttpResponseRedirect('/login/')
                 return response
#进入bug查询列表
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
def bugmore_detail(request, page):
        username = request.COOKIES.get('username', '')
        if username:
            print("进入 bug_detail:", username)
            userdata = models.User.objects.filter(username__contains=username)
            for row in userdata:
                username = row.nickname
                bug_count_list = models.bug.objects.bugmore_detail(page)
            return render_to_response('table_advanced.html', {'username': username,
                                                              'bug_count_list': bug_count_list }
                                      )
        else:
            response = HttpResponseRedirect('/login/')
            return response
#进入jenkins查询列表 commitcode
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
    if username:
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
        if request.method == 'POST':
            print("调 POST")
            date_ff="date >='1700-00-00' and "
            date_tt = " date <='2099-12-31' and "
            object_nn=" object_id in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,99)"
            #获取用户名和密码
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            object_name = request.POST.get('object_name')
            if date_from:
                date_ff="date >='"+date_from+"' and "
            if date_to:
                date_tt=" date <='"+date_to+"' and "
            if object_name:
                object_nn=" object_id='"+object_name+"'"
            sql=date_ff+date_tt+object_nn
            print ("sql:", sql)
            day_statistics_detail_list = models.bug.objects.day_statistics_search_detail(sql)
            print ("day_statistics_detail_list:", day_statistics_detail_list)
        return render_to_response('table_daydata_search.html', {'username': username,
                                                             'day_statistics_detail_list': day_statistics_detail_list}
                                      )
    else:
        response = HttpResponseRedirect('/login/')
        return response
#jenkins数据查询
def jenkins_search(request):
    print("进入:",request)
    username = request.COOKIES.get('username', '')
    jenkins_search_detail_list=''
    if username:
        userdata = models.User.objects.filter(username__contains=username)
        for row in userdata:
            username = row.nickname
        if request.method == 'POST':
            print("调 POST")
            commitcodec=""
            change_namec=""
            date_ff="date >='1700-00-00' and "
            date_tt = " date <='2099-12-31' and "
            object_nn=" object_id in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,99)"
            # 获取数据
            commitcode = request.POST.get('commitcode')
            change_name = request.POST.get('change_name')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            object_name = request.POST.get('object_name')
            if commitcode:
                commitcodec="commitcode like '%"+commitcode+"%' and "
            if change_name:
                change_namec="change_name like '%"+change_name+"%' and "
            if date_from:
                date_ff="date >='"+date_from+"' and "
            if date_to:
                date_tt=" date <='"+date_to+"' and "
            if object_name:
                object_nn=" object_id='"+object_name+"'"
            sql=commitcodec + change_namec + date_ff + date_tt + object_nn
            print ("sql:", sql)
            jenkins_search_detail_list = models.bug.objects.jenkins_search_detail(sql)
            print ("jenkins_search_detail_list:", jenkins_search_detail_list)
        return render_to_response('table_jenkins_search.html', {'username': username,
                                                             'jenkins_search_detail_list': jenkins_search_detail_list}
                                      )
    else:
        response = HttpResponseRedirect('/login/')
        return response
#bug 查询
def bug_search(request):
        print("进入:", request)
        username = request.COOKIES.get('username', '')
        bug_search_detail_list = ''
        if username:
            userdata = models.User.objects.filter(username__contains=username)
            for row in userdata:
                username = row.nickname
            if request.method == 'POST':
                print("调 POST")
                bug_idd=""
                bug_namen=""
                status_s=" bug_status in ('新建','已提交','完成') and "
                date_ff = "date >='1700-00-00' and "
                date_tt = " date <='2099-12-31' and "
                main_object_nn = " type in ('泡面番','大数据系统') and "
                object_nn = " sub_type in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,99)"
                # 获取数据
                bug_id = request.POST.get('bug_id')
                bug_name = request.POST.get('bug_name')
                status = request.POST.get('status')
                date_from = request.POST.get('date_from')
                date_to = request.POST.get('date_to')
                main_object_name = request.POST.get('main_object_name')
                object_name = request.POST.get('object_name')

                if bug_id:
                    bug_idd = "bug_id='" + bug_id + "' and "
                if bug_name:
                    bug_namen = "bug_name like %" + bug_name + "% and "
                if status:
                    status_s = "bug_status ='" + status + "' and "
                if date_from:
                    date_ff = "date >='" + date_from + "' and "
                if date_to:
                    date_tt = " date <='" + date_to + "' and "
                if main_object_name:
                    main_object_nn = " type='" + main_object_name + "' and "
                if object_name:
                    object_nn = " sub_type='" + object_name + "'"
                sql = bug_idd + bug_namen + status_s + date_ff + date_tt + main_object_nn + object_nn
                print("sql:", sql)
                bug_search_detail_list = models.bug.objects.bug_search_detail(sql)
                print("bug_search_detail_list:", bug_search_detail_list)
            return render_to_response('table_bug_search.html', {'username': username,
                                                                'bug_search_detail_list': bug_search_detail_list}
                                      )
        else:
            response = HttpResponseRedirect('/login/')
            return response