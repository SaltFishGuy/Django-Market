from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from hashlib import sha1
from df_user.models import *
from df_goods.models import *
# Create your views here.

def register(request):
    context = {'title':'注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #用户注册的信息
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    if upwd != ucpwd:
        return HttpResponseRedirect('/user/register')
    #对密码原文进行sha1的加密
    #创建sha1对象
    s1 = sha1()
    #对password进行加密
    s1.update(upwd.encode())
    upwd2 = s1.hexdigest()

    #创建模板对象 并填入数据 然后写入数据库中
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail
    user.save()

    return HttpResponseRedirect('/user/login')

def register_exist(request):
    #接受用户传入的uname参数
    get = request.GET
    uname = get.get('uname')

    #在数据库中查找该用户是否存在
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):

    uname = request.COOKIES.get('uname','')

    context = {'title':'登陆','error_name': 0,'error_pwd':0,'uname':uname, 'user_center':1}
    return render(request,'df_user/login.html',context)


from df_user.islogin import islogin


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu')

    #根据用户名和密码查询数据库
    users = UserInfo.objects.filter(uname = uname)
    if len(users)>0:
        #用户存在
        #对密码原文进行sha1的加密
        s1 = sha1()
        s1.update(upwd.encode())
        upwd2 = s1.hexdigest()

        #与数据库中的密码进行比较
        if upwd2 == users[0].upwd:
            #登陆成功
            url = request.COOKIES.get('url', '/user/info')
            red = HttpResponseRedirect(url)

            if jizhu:
                red.set_cookie('uname',uname)# 记住用户名
            else:
                red.set_cookie('uname','')# 没有记住用户名

            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname

            return red

        else:
            #登陆失败
            context = {'title': '登陆','error_name': 0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request, 'df_user/login.html', context)


    else :
        context = {'title': '登陆','error_name': 1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request, 'df_user/login.html', context)

@islogin
def info(request):
    #读取数据库中的用户信息
    user = UserInfo.objects.get(id = request.session['user_id'])
    user_name = user.uname
    user_address = user.uaddress
    user_phone = user.uphone
    #从cookies中读取最近浏览的信息
    goods_ids = request.COOKIES.get('goods_ids')
    #判断cookie中的最近浏览商品序列是否为空
    if goods_ids and goods_ids!='':
        #不为空 以逗号隔开
        goods_ids = goods_ids.split(',')
    else :
        #为空
        goods_ids=[]
    #根据goods_ids中商品的id去数据库中查询 找出商品对象
    goods_list=[]
    for id in goods_ids:
        goods = GoodsInfo.objects.get(id = id)
        goods_list.append(goods)

    context= {'title':'用户中心',
              'user_name':user_name,
              'user_address':user_address,
              'user_phone':user_phone,
              'info':1,
              'user_center':1,
              'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)

@islogin
def order(request):
    context={'order':1,'user_center':1}
    return render(request,'df_user/user_center_order.html',context)

@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()

    phone = user.uphone[:3] + 4*'*' +user.uphone[-4:]
    context={'site':1,
             'ushou':user.ushou,
             'uaddress':user.uaddress,
             'uyoubian':user.uyoubian,
             'uphone':phone,
             'title':'用户中心',
             'user_center': 1,
             }
    return render(request,'df_user/user_center_site.html',context)

def logout(request):
    request.session.flush()#清理session缓存
    return HttpResponseRedirect('/user/login')