from django.contrib.auth.decorators import login_required
from utils.response import json_response
from article.models import Article
from comment.models import Comment
from message.models import UserMessage


@login_required
def create_comment(request):
    article_id = int(request.POST["article_id"])
    content = request.POST["content"].strip()
    to_comment_id = int(request.POST["to_comment_id"])
    article = Article.objects.get(id=article_id)
    if to_comment_id != 0:
        to_comment = Comment.objects.get(id=to_comment_id)
        new_msg = UserMessage(owner=to_comment.owner,
                content="有人回复了你的评论'%s'" % to_comment.content[:30],
                link="http://%s/article/list/detail/%s" % (request.get_host(),
                article.id))
        new_msg.save()
    else:
        to_comment = None
        new_msg = UserMessage(owner=article.owner,
                content="有人回复了你的文章'%s'" % article.title,
                link="http://%s/article/list/detail/%s" % (request.get_host(),
                article.id))
        new_msg.save()
    if not content:
        return json_response({"status": "error",
                "msg": "评论内容不能为空."})
    comment = Comment(article=article, owner=request.user,
            content=content, to_comment=to_comment)
    comment.save()
    return json_response({"status": "ok", "msg": ""})
