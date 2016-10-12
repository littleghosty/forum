from django.contrib.auth.decorators import login_required
from utils.response import json_response
from article.models import Article
from comment.models import Comment


@login_required
def create_comment(request):
    article_id = int(request.POST["article_id"])
    content = request.POST["content"].strip()
    article = Article.objects.get(id=article_id)
    if not content:
        return json_response({"status": "error",
                "msg": "评论内容不能为空."})
    comment = Comment(article=article, owner=request.user,
            content=content)
    comment.save()
    return json_response({"status": "ok", "msg": ""})
