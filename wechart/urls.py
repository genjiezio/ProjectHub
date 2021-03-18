from django.urls import path, re_path

from wechart.views import *

app_name = 'wechart'
urlpatterns = [
    path('login/', loginView.as_view()),
    path('verify/', verifyView.as_view()),
    path('create/', createView.as_view()),
    path('logout/', logoutView.as_view()),
    path('get_project/', getProjectView.as_view()),
    path('check_group/', checkGroupView.as_view()),
    path('join_group/', joinGroupView.as_view()),
    path('get_grouppage/', getGroupPageView.as_view()),
    path('get_mygroup/', getMyGroupView.as_view()),
    path('get_getmessage/', getMessageView.as_view()),
    path('readmessage/', readMessageView.as_view()),
]
