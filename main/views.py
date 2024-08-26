from django.shortcuts import render, redirect
from . import models
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ArticleForm
from django.db.models import Count

def get_most_liked_articles(num_articles=5):
    most_liked_articles = models.Article_like.objects.values('article_like') \
        .annotate(like_count=Count('id')) \
        .order_by('-like_count')[:num_articles]
    
    article_ids = [item['article_like'] for item in most_liked_articles]
    most_liked_articles = models.Arcticle.objects.filter(id__in=article_ids)

    return most_liked_articles

def index(request):
    # count user in USER model
    user_count = User.objects.count()
    article_count = models.Arcticle.objects.count()
    most_liked_articles = get_most_liked_articles()
    context = {'user_count': user_count, 'article_count': article_count,'most_liked_articles': most_liked_articles}
    return render(request, 'index.html',context)

def article_list(request):
    article_list = None
    if request.method == 'POST':
        article = request.POST['article']
        article_list = models.Arcticle.objects.filter(title__icontains=article)
    else:
        article_list = models.Arcticle.objects.all()[:5]
    categories = models.ArticleCategory.objects.all()
    context = {'article_list': article_list, 'categories': categories}
    return render(request, 'article.html', context)

def article_by_category(request, category_id):
    articles= models.Arcticle.objects.filter(category_id=category_id)
    categories = models.ArticleCategory.objects.all()
    context = {'article_list': articles, 'categories': categories}
    return render(request, 'article.html', context)
    
@login_required(login_url='go_to_login')  
def liked(request, article_id):
    try:
        article = models.Arcticle.objects.filter(id=article_id).first()
    except ValueError:
        return redirect('error')

    user = request.user
    like_exists = models.Article_like.objects.filter(article_like=article, user=user).exists()

    if not like_exists:
        models.Article_like.objects.create(article_like=article, user=user)
    else:
        return redirect('article_detail', article_id=article_id)
    return redirect('article_detail', article_id=article_id) 

  
def go_to_login(request):   
    return render(request, 'login_required.html')

def base(request):   
    return render(request, 'base.html')

def about1(request):   
    return render(request, 'about1.html')

def search_article(request):
    if request.method == 'POST':
        article = request.POST['makala']
        articles = models.Arcticle.objects.filter(title__icontains=article)
        categories = models.ArticleCategory.objects.all()
        context = {'article_list': articles, 'categories': categories}
        return render(request,'article.html', context)

def article_detail(request, article_id):
    article = models.Arcticle.objects.filter(id=article_id).first()
    article_comments = models.Article_comment.objects.filter(article_comment__id=article_id)
    context = {'article': article,'article_id':article_id, 'article_comments':article_comments}
    return render(request, 'article_detail.html', context)


@login_required(login_url='go_to_login')
def article_comment(request,article_id):
    print('comment_page')
    if request.method == 'POST':
        print('post method is work')
        article = models.Arcticle.objects.filter(id=article_id).first()
        user = request.user
        comment = request.POST['comment']
        models.Article_comment.objects.create(article_comment=article, user=user, comment=comment)
    
    return redirect('article_detail', article_id=article_id)

def http404(request):
    return render(request, 'http404.html')


def contact(request):
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        user = request.user
        result = models.Contact.objects.create(title=title, message=message, user=user)
        if result:
           message = messages.success(request, 'Habar üçin sagboluň!.')
        else:
            message = messages.error(request, 'Näsazlyk ýüze çykdy.')
        return render(request, 'contact.html', {'message': message})

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def profile(request):
    articles = models.Arcticle.objects.filter(user_name__icontains=request.user.username)
    print(articles)
    categories = models.ArticleCategory.objects.all()
    form = ArticleForm()
    
    context = {'categories': categories, 'form': form,'articles': articles}
    return render(request, 'profile.html',context)


def add_article(request):
    if request.method == 'POST':
       form = ArticleForm(request.POST, request.FILES)
       if form.is_valid():
           article = form.save(commit=False)
           article.user_name = request.user.username
           article.save()
           return redirect('profile')
       