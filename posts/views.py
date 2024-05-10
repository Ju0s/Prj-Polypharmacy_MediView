from django.shortcuts import render, redirect
from posts.models import Post
from posts.forms import PostForm

# Create your views here.
def ask(request):
    #요청으로부터 사용자 정보를 가져온다.
    user = request.user
    
    #가져온 사용자가 '로그인 했는지' 여부를 가져온다.
    is_authenticated = user.is_authenticated
    
    #요청에 포함된 사용자가 로그인하지 않은 경우
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'posts/ask.html',context)

def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # save but do not commit to db yet
            new_post.user = request.user        # assign the user from request
            new_post.save()                     # now save it to the db
            return redirect('/posts/ask/')  # redirect to a new URL
    else:
        form = PostForm()
    return render(request, 'posts/post_add.html', {'form': form})
