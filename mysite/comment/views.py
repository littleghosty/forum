from django.contrib.auth.decorators import login_required
from utils.response import json_response
from article.models import Article
from comment.models import Comment


@login_required
def create_comment(request):
    article_id = int(request.POST["article_id"])
    content = request.POST["content"].strip()
    to_comment_id = int(request.POST["to_comment_id"])
    article = Article.objects.get(id=article_id)
    if to_comment_id != 0:
        to_comment = Comment.objects.get(id=to_comment_id)
    else:
        to_comment = None
    if not content:
        return json_response({"status": "error",
                "msg": "评论内容不能为空."})
    comment = Comment(article=article, owner=request.user,
            content=content, to_comment=to_comment)
    comment.save()
    return json_response({"status": "ok", "msg": ""})
