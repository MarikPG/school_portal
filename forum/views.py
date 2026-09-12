from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Thread, Post

def forum_home(request):
    threads = Thread.objects.select_related('user').order_by('-updated_at')
    return render(request, 'forum/forum_home.html', {'threads': threads})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration/signup.html', {'form': form})

def thread_list(request):
    threads = Thread.objects.select_related('user').order_by('-updated_at')
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.select_related('user').prefetch_related('likes', 'dislikes').order_by('created_at')
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
            return redirect('forum:thread_detail', thread_id=thread.id)

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
            return redirect('forum:thread_list')

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
            return redirect('forum:thread_detail', thread_id=thread.id)

    return render(request, 'forum/edit_thread.html', {'thread': thread, 'error': error})

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied("Видаляти гілки можуть лише адміністратори та модератори.")

    if request.method == 'POST':
        thread.delete()
        return redirect('forum:thread_list')

    return render(request, 'forum/delete_thread.html', {'thread': thread})


@login_required
def react_to_post(request, post_id, reaction):
    if request.method != 'POST' or reaction not in {'like', 'dislike'}:
        return redirect('forum:index')

    post = get_object_or_404(Post, id=post_id)
    own_reaction = post.likes if reaction == 'like' else post.dislikes
    opposite_reaction = post.dislikes if reaction == 'like' else post.likes

    if own_reaction.filter(id=request.user.id).exists():
        own_reaction.remove(request.user)
    else:
        own_reaction.add(request.user)
        opposite_reaction.remove(request.user)

    return redirect('forum:thread_detail', thread_id=post.thread_id)