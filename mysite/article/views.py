from django.shortcuts import render, redirect
from .models import Block, Article
from .forms import ArticleForm
from utils.paginator import paginator_queryset


def article_list(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    page_no = int(request.GET.get("page_no", "1"))
    articles_objs = Article.objects.filter(block=block, status=0).order_by("-last_update_timestamp")
    object_list, pagination_data = paginator_queryset(articles_objs, page_no)
    return render(request, "article_list.html", {"articles": object_list,
                            "b": block, "pagination": pagination_data})


def create_article(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    if request.method == "GET":
        return render(request, "create_article.html", {"b": block, })
    else:
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.block = block
            article.status = 0
            article.save()
            return redirect("/article/list/%s" % block_id)
        else:
            return render(request, "create_article.html", {"b": block,
                "form": form})


def article_detail(request, article_id):
    article_id = int(article_id)
    article = Article.objects.get(id=article_id)
    block = article.block
    return render(request, "article_detail.html", {"article": article,
        "b": block})
