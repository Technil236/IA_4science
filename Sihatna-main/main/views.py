from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Forum, Post, Reply
from accounts.models import User
from .forms import PostForm, ReplyForm
from django.db.models import Q
from django.db.models import Count

def home(request):
    user = request.user

    forum = Forum.objects.all()

    forums = Forum.objects.annotate(total_posts=Count('post'))

    forums = forums.order_by('-total_posts')

    most_active_forum = forums.first()

    most_recent_post = Post.objects.filter(approuved=True).order_by('-date').first()
  

    context = {
        'forum': forum,
        'most_active_forum': most_active_forum,
        'most_recent_post':most_recent_post,
    }

    return render(request, 'home.html', context)


def detail(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    posts = Post.objects.filter(approuved=True, forum=forum)
    # Calcule du nombre de reponses pour chaque post
    posts = posts.annotate(nom_replies=Count('reply'))
    # Trie des posts en fonction du nombre de réponses en ordre décroissant
    posts = posts.order_by('-nom_replies')

    recent_post = posts.filter(approuved=True).order_by('-date').first()

    context ={
        "forum":forum,
        "posts":posts,
        "most_active_post":posts.first(),
        "recent_post":recent_post,
    }
    return render(request, 'detail.html', context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    replies = Reply.objects.filter(post=post)
    
    author = request.user

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data["reply"]
            new_reply, created = Reply.objects.get_or_create(author=author, content=reply_text, post=post)

    else:
        form = ReplyForm()  # Créez une instance du formulaire pour afficher le formulaire vide

    context = {
        "post": post,
        "replies": replies,
        "form": form,  # Assurez-vous de passer le formulaire au contexte pour l'affichage
    }

    return render(request, 'post.html', context)



@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("home")
    context.update({
        "form":form,
        "title":"Create New Post"
    })
    return render(request, "create_post.html", context)


def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        forums = Forum.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        replies = Reply.objects.filter(content__icontains=query)

        results = {
            "forums":forums,
            "posts":posts,
            "replies":replies,
        }

    context = {
        "query":query,
        "results":results,
    }

    return render(request, 'search.html', context)

def not_found(request):
    return render(request, 'not_found.html')