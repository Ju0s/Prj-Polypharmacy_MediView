from django.shortcuts import render, redirect
from users.forms import LoginForm

# Create your views here.
def login_view(request):
    #이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect('/posts/ask/')
    return render(request,'users/login.html')

    #로그인 폼 인스턴스 생성
    form = LoginForm()
    context = {
        'form' : form,
    }
    return render(request, 'users/login.html',context)
