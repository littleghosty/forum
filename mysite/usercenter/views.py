from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ActivateCode
import uuid
import os
from django.http import HttpResponse
import datetime


def register(request):
    error = ""
    if request.method == "GET":
        return render(request, "user_register.html")
    else:
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        re_password = request.POST['re_password'].strip()
        if not username or not password or not email:
            error = "任何字段都不能为空"
        if password != re_password:
            error = "两次密码不一致"
        if User.objects.filter(username=username).count() > 0:
            error = "用户已存在"
        if User.objects.filter(email=email).count() > 0:
            error = "该邮箱已注册"
        if not error:
            user = User.objects.create_user(username=username,
                    email=email, password=password)
            user.is_active = False
            user.save()
            new_code = str(uuid.uuid4()).replace("-", "")
            expire_time = datetime.datetime.now() + datetime.timedelta(days=2)
            code_record = ActivateCode(owner=user, code=new_code,
                                       expire_timestamp=expire_time)
            code_record.save()
            activate_link = "http://%s%s" % (request.get_host(), reverse(
                                        "user_activate", args=[new_code]))
            send_mail('[python论坛]激活邮件',
                      '您的激活链接为: %s' % activate_link,
                      'huyuanxuan@163.com',
                      [email],
                      fail_silently=False)
        else:
            return render(request, "user_register.html", {"error": error})
        return HttpResponse("请查收邮件激活帐户！")


def activate(request, code):
    query = ActivateCode.objects.filter(code=code,
                                 expire_timestamp__gte=datetime.datetime.now())
    if query.count() > 0:
        code_record = query[0]
        code_record.owner.is_active = True
        code_record.owner.save()
        return HttpResponse("激活成功")
    else:
        return HttpResponse("激活失败")


@login_required
def upload_avatar(request):
    if request.method == "GET":
        return render(request, "upload_avatar.html")
    else:
        profile = request.user.userprofile
        avatar_file = request.FILES.get("avatar", None)
        if not avatar_file:
            return HttpResponse("未选择文件")
        file_name = request.user.username + avatar_file.name
        if avatar_file.size > 50000:
            return HttpResponse("图片大小不能超过500KB")
        file_path = os.path.join("/usr/share/userres/avatar/", file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)
        url = "http://res.myforum.com/avatar/%s" % file_name
        profile.avatar = url
        profile.save()
        return redirect("/")
