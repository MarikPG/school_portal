from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Thread, Post

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

@login_required
def create_thread(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied("Ви не маєте прав для створення нової теми.")

    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if len(title) < 5 or len(content) < 5:
            error = "Заголовок та вміст повинні містити щонайменше 5 символів."
        else:
            Thread.objects.create(
                title=title,
                content=content,
                user=request.user
            )
            return redirect('thread_list')

    return render(request, 'forum/create_thread.html', {'error': error})

@login_required
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied("Редагувати гілки можуть лише адміністратори та модератори.")

    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if len(title) < 5 or len(content) < 5:
            error = "Заголовок та вміст повинні містити щонайменше 5 символів."
        else:
            thread.title = title
            thread.content = content
            thread.save()
            return redirect('thread_detail', thread_id=thread.id)

    return render(request, 'forum/edit_thread.html', {'thread': thread, 'error': error})

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied("Видаляти гілки можуть лише адміністратори та модератори.")

    if request.method == 'POST':
        thread.delete()
        return redirect('thread_list')

    return render(request, 'forum/delete_thread.html', {'thread': thread})