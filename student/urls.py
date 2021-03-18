from django.urls import path, re_path

from student.views import *
from student.group_views import *
from student.info_views import *

app_name = 'student'
urlpatterns = [
    re_path(r'find_account$', Account_Operation.create_account),
    re_path(r'verify$', Account_Operation.verify),
    re_path(r'check_account$', Account_Operation.check_account),
    re_path(r'login_out$', Account_Operation.log_out),

    re_path(r'add_info_skill$', Label_Operation.add_label),
    re_path(r'get_info_skill$', Label_Operation.get_label),
    re_path(r'delete_info_skill$', Label_Operation.remove_label),


    re_path(r'add_project_label$', Label_Operation.add_project_label),
    re_path(r'get_project_label$', Label_Operation.get_project_label),

    re_path(r'get_course$', Course_Operation.get_course),
    re_path(r'create_team$', Group_Operation.create_group),
    re_path(r'get_team$', Group_Operation.get_project_group),
    re_path(r'join_team$', Group_Operation.join_group),

    re_path(r'get_homepage$', Homepage.get_homepage),
    re_path(r'get_info_project$', Homepage.get_terminal_project),



    path('project_page', project_page),
    path('file_upload', file_upload),
    path('file_download', file_download),
    path('file_delete', file_delete),
    path('edit_user', edit_user),
    path('get_info_user', get_info_user),
    path('member_delete', member_delete),
    path('group_delete', group_delete),
    path('get_message', get_message),
    path('confirm_msg', confirm_msg),
    path('change_group_name', change_group_name),
    path('choose_time', choose_time),
]
