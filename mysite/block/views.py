from django.shortcuts import render
from .models import Block


def block_list(request):
    blocks = Block.objects.all().order_by("-id")
    return render(request, "block_list.html", {"blocks": blocks})
