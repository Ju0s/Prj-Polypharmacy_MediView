from django.shortcuts import render

# Create your views here.
def ask(request):
    #요청으로부터 사용자 정보를 가져온다.
    user = request.user
    
    #가져온 사용자가 '로그인 했는지' 여부를 가져온다.
    is_authenticated = user.is_authenticated
    
    print('user:',user)
    print('is_authenticated:',is_authenticated)
    return render(request,'posts/ask.html')
