from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def sendEmail(request):
    return render(request, 'index.html')


def send_email(request):
    # 值1：  邮件标题   值2： 邮件主体
    # 值3： 发件人      值4： 收件人
    res = send_mail('关于中秋节放假通知',
                    '中秋节放三天假',
                    '11811522@mail.sustech.edu.cn',
                    ['275137858@qq.com'])
    if res == 1:
        return HttpResponse('邮件发送成功')
    else:
        return HttpResponse('邮件发送失败')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == "root" and pwd == "123":
            if request.POST.get('box') == "1":  # checkbox被按下
                request.session.set_expiry(3600)  # session认证时间为10s，10s之后session认证失效
            request.session['username'] = user  # user的值发送给session里的username
            request.session['is_login'] = True  # 认证为真
            return redirect('/index')
        else:
            return redirect('/login')
    return render(request, 'in.html')

@csrf_exempt
def index(request):
    if request.session.get('is_login', None):  # 若session认证为真

        return render(request, 'in.html', {'username': request.session['username']})
    else:
        return HttpResponse('滚')


def logout(request):  # 撤销
    request.session.clear()  # 删除session里的全部内容
    return redirect('/login')
