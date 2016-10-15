from django.shortcuts import render
from .models import Block
from message.models import UserMessage


def block_list(request):
    blocks = Block.objects.all().order_by("-id")
    if request.user.is_authenticated():
        msg_cnt = UserMessage.objects.filter(status=0, owner=request.user).count()
    else:
        msg_cnt = 0
    return render(request, "block_list.html", {"blocks": blocks,
        "msg_cnt": msg_cnt})
