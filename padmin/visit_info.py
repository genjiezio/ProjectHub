from django.utils import timezone

from padmin.models import UserIP, DayNumber
from .ip_convert_addr import ip_to_addr


# 自定义的函数，不是视图
def record_visit_info(request, account, character):
    # 记录访问 ip 和每个 ip 的次数

    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    # print(client_ip)

    ip_exist = UserIP.objects.filter(ip=str(client_ip), account=account, character=character)

    if ip_exist:  # 判断是否存在该 ip
        user = ip_exist[0]
    else:
        user = UserIP()
        user.ip = client_ip
        user.account = account
        user.character = character
        try:
            user.ip_addr = ip_to_addr(client_ip)
        except:
            user.ip_addr = 'unknown'
    user.save()

    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date, user=user)
    if today:
        dayuser = today[0]
        dayuser.count += 1
    else:
        dayuser = DayNumber()
        dayuser.dayTime = date
        dayuser.user = user
        dayuser.count = 1
    dayuser.save()
