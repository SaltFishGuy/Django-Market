from django.shortcuts import render
from df_cart.models import *
from django.http import JsonResponse
from df_user.models import *

# Create your views here.


def cart(request):
    #从session中获取当前用户的id
    uid  = request.session.get('user_id')
    #根据id搜索当前用户放入购物车中的品种
    carts = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车',
               'user_center':1,
               'carts':carts}
    return render(request,'df_cart/cart.html',context)


def add(request,gid,count):
    #从session中获取用户id
    uid = request.session.get('user_id')
    count = int(count)#字符串转成整数

    #从数据库中根据uid和gid读取商品数量
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid) #carts数量要么是0要么是1
    if len(carts) >= 1:
        #购物车中已经有商品
        cart = carts[0] #该商品是一个列表加字典。
        cart.count += count
        cart.save()

    else:
        #购物车中没有商品
        cart=CartInfo()
        cart.user_id = uid
        cart.goods_id =gid
        cart.count = count
        cart.save()



    result = CartInfo.objects.filter(user_id=uid).count()

    return JsonResponse({'count':result}) #一共有多少个商品

def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.get(id = cart_id)
        cart.count = int(count)
        cart.save()
        data = {'ok':1}
    except Exception:
        data = {'ok':0}


    return JsonResponse(data)

def delete(request,cart_id):
    try:
        data = {'ok':1}
        cart = CartInfo.objects.filter(id=cart_id)
        cart.delete()
        cart.save()

    except Exception:
        data = {'ok': 0}

    return JsonResponse(data)


def order(request):
    # 从session中获取当前用户的id
    #uid = request.session.get('user_id')
    # 根据id搜索当前用户放入购物车中的品种
   # carts = CartInfo.objects.filter(user_id=uid)
    carts = CartInfo.objects.filter(jug='false')
    #收件人信息
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        for item in carts:
            if post.get('check') =='None':
                item.jug = post.get('check')
                item.save()

    phone = user.uphone[:3] + 4 * '*' + user.uphone[-4:]
    context = {
        'title': '提交订单',
        'user_center':1,
        'carts':carts,
        'site': 1,
        'ushou': user.ushou,
        'uaddress': user.uaddress,
        'uyoubian': user.uyoubian,
        'uphone': phone,


    }
    return render(request,'df_cart/place_order.html',context)
