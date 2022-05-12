from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from boardapp.models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.
'''
def signupfunc(request):
    #これはClassBaedViewにおいてmodel = hogeとしたのと同じように考えることができる
    #この定義によってモデルの中のオブジェクトの要素を扱うことができるようになる
    object = User.objects.get(username = 'takamoto')
    print(object.email)

    if request.method == "POST":
        print("this is POST method")
    else:
        print('this is not post method')
        print(request.method)
    return  render(request, 'signup.html', {'some' : 100} )

'''
def signupfunc(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        #重複したユーザが登録された時の挙動
        
        try:
            user = User.objects.create_user(username, '', password)
            return  render(request, 'signup.html', {'some' : 100} )
        except IntegrityError:
            return  render(request, 'signup.html', {'error' : "このユーザはすでに登録されています"} )
       
        #print(username)
        #print(password)
    #redirectで同じ関数を呼び出すと無限ループに入ってしまう
    #renderはcontextが違うものを入れる. 
    #redirectは何らかの処理が終わって違うところに遷移させる際に用いる
    #return  redirect('login')
    return render(request, 'signup.html')

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return  redirect('list')
        else:
            return  render(request, 'login.html', {} )
    return  render(request, 'login.html', {'context' : 'not logged in'} )


#ログインしているかどうかを判定するには2つ方法がある
#1つ目は以下のようにlogin_requiredデコレータを用いる方法

#@login_required

#2つ目はtemplateでdjangoの書式を用いて条件分岐を行う方法
#(今はこっちで動かしている)

def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
   #db内のデータを取ってくるときに
   #objct = BoardModel.object.get('')
   #でもいいが以下のようにdjangoに備わっている関数を用いることもできる
   #番号に沿ったオブジェクトを返すか, なかったらエラーを返す
   object = get_object_or_404(BoardModel, pk=pk)
   return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    #以下はget_object_or_404でも良い
    object = BoardModel.objects.get(pk=pk)
    object.good += 1
    #変更をモデルのオブジェクトに反映する
    object.save()
    return redirect('list')

def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else:
        object.read += 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'snsimage')
    success_url = reverse_lazy('list')