from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt
import json

from padmin.visit_info import record_visit_info
from teacher.models import Teacher

class Relogin():
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            session_cache = caches['t_session']
            if not request.session.get('account'):
                response = {}
                response['msg'] = 'Please login.'
                response['status'] = 307
                return JsonResponse(response)

            account = request.session['account']
            sessionid = request.session.session_key
            data = session_cache.get(key=account)
            if sessionid != data:
                response = {}
                response['msg'] = 'Your account is logged in elsewhere.'
                response['status'] = 306
                print(sessionid)
            return JsonResponse(response)
        except Exception as e:
            pass
        return self.func(request)

@require_http_methods(["POST"])
def check_account(request):
    response = {}
    session_cache = caches['t_session']
    if request.method == 'POST':
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            account = post_content["name"]
            password = post_content["password"]
            teacher = Teacher.objects.get(account=account)
            if check_password(password, teacher.password):
                record_visit_info(request, account, 'teacher')
                data = session_cache.get(teacher.account)
                request.session.set_expiry(0)
                request.session['account'] = teacher.account
                request.session['is_login'] = True
                sessionid = request.session.session_key
                if data and data != sessionid:
                    response['msg'] = 'Warning: Your account is already logged in elsewhere.'
                    response['status'] = 207
                else:
                    response['msg'] = 'success'
                    response['status'] = 200
                response['tid'] = teacher.id
                session_cache.set(key=teacher.account, value=sessionid,
                                  timeout=request.session.get_expiry_age())

                # db_cache.delete(key=student.account)
            else:
                response['msg'] = 'wrong'
                response['status'] = 1000
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
    return JsonResponse(response)

def log_out(request):
    response = {}
    try:

        account = request.session.get('account')
        session_cache = caches['t_session']
        session_cache.delete(key=account)
        response['msg'] = 'success'
        response['status'] = 200
    except Exception as e:
        response['msg'] = str(e)
        response['status'] = 1000
    return JsonResponse(response)