from django.http import HttpResponse,HttpResponseRedirect

def islogin(func):
    def login_func(request,*args,**kwargs):
        #判断是否登陆
        if request.session.get('user_id'):
            #用户已经登陆 可以正常访问页面
            return func(request,*args,**kwargs)
        else:
            # 用户未登录 跳转到登录页面
            red = HttpResponseRedirect('/user/login')
            # 获取用户尝试访问的路径
            path = request.get_full_path()
            # 把该路径存到cookie中
            red.set_cookie('url', path)

            return red

    return login_func