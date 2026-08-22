from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Thread, PostІ

# Create your views here.

def forum_home(request):
    threads = Thread.objects.all()
    return render(request, 'forum/forum_home.html', {'threads': threads})

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().order_by('created_at')
    error = None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        content = request.POST.get('content', '').strip()
        
        if len(content) < 2:
            error = "Повідомлення занадто коротке."
        else:
            Post.objects.create(
                thread=thread,
                user=request.user,
                content=content
            )
            return redirect('thread_detail', thread_id=thread.id)

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'posts': posts,
        'error': error
    })