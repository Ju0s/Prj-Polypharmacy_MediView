from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
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

@login_required
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

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to view this page.")
    
    comments = post.comment_set.all().order_by('-created')
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.user = request.user
        new_comment.save()
        return redirect('post_detail', post_id=post_id)
    
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})
