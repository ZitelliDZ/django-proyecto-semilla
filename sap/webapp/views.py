from django.http import HttpResponse
from django.shortcuts import redirect, render

from webapp.decorators import user_is_superuser
from .models import Article, ArticleSeries
from .form import SeriesUpdateForm,SeriesCreateForm,ArticleCreateForm,ArticleUpdateForm


# Create your views here.


def homepage(request):
    matching_series = ArticleSeries.objects.all()
    return render(
        request=request,
        template_name="webapp/home.html",
        context={"objects": matching_series, "title": "Home Page",'type':'Series'},
    )


def series(request, series: str):
    matching_series = Article.objects.filter(series__slug=series).all()
    return render(
        request=request,
        template_name="webapp/home.html",
        context={"objects": matching_series, "title": "Series Page",'type':'Artículos'},
    )


def article(request, series: str, article: str):
    matching_article = Article.objects.filter(
        series__slug=series, article_slug=article
    ).first()
    return render(
        request=request,
        template_name="webapp/article.html",
        context={"object": matching_article, "title": "Article Page"},
    )


@user_is_superuser(redirect_url='homepage')
def new_series(request):
    if request.method == "POST":
        form = SeriesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
         form = SeriesCreateForm()
    return render(
        request=request,
        template_name='webapp/new_record.html',
        context={
            "object": "Series",
            "form": form
            }
        )

@user_is_superuser(redirect_url='homepage')
def new_post(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"{form.cleaned_data['series'].slug}/{form.cleaned_data.get('article_slug')}")
    else:
         form = ArticleCreateForm()
    return render(
        request=request,
        template_name='webapp/new_record.html',
        context={
            "object": "Artículos",
            "form": form
            }
        )

@user_is_superuser(redirect_url='homepage')
def series_update(request,series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        form = SeriesUpdateForm(request.POST, request.FILES, instance=matching_series)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    
    else:
        form = SeriesUpdateForm(instance=matching_series)

        return render(
            request=request,
            template_name='webapp/new_record.html',
            context={
                "object": "Series",
                "form": form
                }
            )
@user_is_superuser(redirect_url='homepage')
def series_delete(request,series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        matching_series.delete()
        return redirect('homepage')
    else:
        return render(
            request=request,
            template_name='webapp/confirm_delete.html',
            context={
                "object": matching_series,
                "type": "Series"
                }
            )
@user_is_superuser(redirect_url='homepage')
def article_update(request, series, article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()
    if request.method == "POST":
        form = ArticleUpdateForm(request.POST, request.FILES, instance=matching_article)
        if form.is_valid():
            form.save()
            return redirect(f'/{matching_article.slug}')
    else:
        form = ArticleUpdateForm(instance=matching_article)
        return render(
            request=request,
            template_name='webapp/new_record.html',
            context={
                "object": "Artículo",
                "form": form
                }
            )

@user_is_superuser(redirect_url='homepage')
def article_delete(request,series,article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    if request.method == "POST":
        matching_article.delete()
        return redirect('homepage')
    else:
        return render(
            request=request,
            template_name='webapp/confirm_delete.html',
            context={
                "object": matching_article,
                "type": "Artículo"
                }
            )