from django.shortcuts import render, redirect
from users.forms import LoginForm
# Create your views here.
def login_view(request):
    #이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect('/posts/ask/')
    if request.method == 'POST':
        #LoginForm 인스턴스 생성, 입력 데이터는 request.POST 사용
        form = LoginForm(data=request.POST)
        
        #LoginForm에 들어온 데이터가 적정한지 유효성 검사
        print('form.is_valid()', form.is_valid())
        
        #유효성 검사 이후에는 cleaned_data에서 데이터를 가져와서 사용
        print('form.cleaned_data:', form.cleaned_data)
        context = {'form':form}
        return render(request, 'users/login.html',context)
    else:
        #로그인 폼 인스턴스 생성
        form = LoginForm()
        context = {
            'form' : form,
        }
        return render(request,'users/login.html',context)