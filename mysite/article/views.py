from django.shortcuts import render, redirect
from .models import Block, Article
from .forms import ArticleForm


def article_list(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    articles_objs = Article.objects.filter(block=block, status=0).order_by("-id")
    return render(request, "article_list.html", {"articles": articles_objs, "b": block})


def create_article(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    if request.method == "GET":
        return render(request, "create_article.html", {"b": block, })
    else:
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article(block=block, title=form.cleaned_data["title"],
                    content=form.cleaned_data["content"], status=0)
            article.save()
            return redirect("/article/list/%s" % block_id)
        else:
            return render(request, "create_article.html", {"b": block,
                "form": form})
