from django.http import JsonResponse, HttpResponseRedirect
from django.middleware.csrf import get_token


# Create your views here.

def get_csrf_token(request):
    return JsonResponse({'csrf_token': get_token(request) or 'NOTPROVIDED'})
