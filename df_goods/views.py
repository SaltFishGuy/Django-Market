from django.shortcuts import render
from df_goods.models import *
from df_cart.models import *
# Create your views here.
def index(request):
    fruit = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[:4]#最新产品
    fruit2 = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[:3]  # 热销产品
    fish = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[:4]  # 最新产品
    fish2 = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[:3]  # 热销产品
    meat = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[:4]  # 最新产品
    meat2 = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[:3]  # 热销产品
    egg = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[:4]  # 最新产品
    egg2 = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[:3]  # 热销产品
    vegetable = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[:4]  # 最新产品
    vegetable2 = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[:3]  # 热销产品
    frozen = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[:4]  # 最新产品
    frozen2 = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[:3]  # 热销产品
    uid = request.session.get('user_id')
    result = CartInfo.objects.filter(user_id=uid).count()


    context = {"title":"首页","guest_cart":1,
               'fruit':fruit,'fruit2':fruit2,
               'fish':fish,'fish2':fish2,
               'meat':meat,'meat2':meat2,
               'frozen':frozen,'frozen2':frozen2,
               'vegetable':vegetable, 'vegetable2':vegetable2,
               'egg':egg,'egg2':egg2,
               'num':result,
               }
    return render(request,'df_goods/index.html',context)

from django.core.paginator import Paginator
def goodlist(request,typeid,pageid,sort):
    #获取产品类型
    goodType = TypeInfo.objects.get(id = typeid)
    #获取最新发布的产品
    newgood = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')[:2] #获取数据传到模板中
    #获取所有产品并按默认排序
    if sort =='1':
        sumgoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')
    elif sort =='2':
        sumgoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('gprice')
    elif sort == '3':
        sumgoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-gclick')
        #分页 15个一页
    paginator = Paginator(sumgoodList,15)
    goodList=paginator.page(int(pageid))
    pindexlist=paginator.page_range
    uid = request.session.get('user_id')
    result = CartInfo.objects.filter(user_id=uid).count()
    context = {'title':'商品列表',
               'guest_cart':1,
               'newgood':newgood,
               'goodList':goodList,
               'sort':sort,
               'typeid':typeid,
               'pindexlist':pindexlist,
               'pageid':int(pageid),
               'goodType':goodType,
               'num': result
               }
    return render(request,'df_goods/list.html',context)

def detail(request,id):
    #获取产品类型id
    typeid=GoodsInfo.objects.get(id = id ).gtype_id
    #获取最新产品类型
    newgood = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')[:2]
    #获取产品类型
    goodType = TypeInfo.objects.get(id=typeid)
    #获取当前商品的对象
    goods = GoodsInfo.objects.get(id=id)
    #增加访问量 点击量
    goods.gclick+=1
    goods.save()
    uid = request.session.get('user_id')
    result = CartInfo.objects.filter(user_id=uid).count()

    context = {'title':'商品详情',
               'guest_cart':1,
               'newgood':newgood,
               'typeid':typeid,
               'goodType': goodType,
               'g':goods,
               "isDetail":1,
                'num':result
               }


    response =  render(request,'df_goods/detail.html',context)
    #读取请求的cookie
    goods_ids = request.COOKIES.get('goods_ids')
    #判断cookie中的商品id序列是否为空
    if goods_ids and goods_ids!='':
        goods_ids = goods_ids.split(',')
        #如果列表中已经有当前id则需要删除列表中原来的id
        if id in goods_ids:
            goods_ids.remove(id)
        #把当前的id插入到列表的最前面
        goods_ids.insert(0,id)
        #取前五个
        if len(goods_ids) >5:
            goods_ids=goods_ids[:5]
    else :
        goods_ids = id
    #转字符串 使用，来连接列表中的每一个元素
    goods_ids = ','.join(goods_ids)
    #添加cookie信息
    response.set_cookie('goods_ids',goods_ids)

    return response