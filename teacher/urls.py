from django.urls import path, re_path

from teacher.account_view import *
from teacher.project_view import *
from teacher.views import *

app_name = 'teacher'
urlpatterns = [

    re_path(r'check_account$', check_account),
    re_path(r'promanage$', Teacher_Page.get_teacher_page),
    re_path(r'login_out$', log_out),

    re_path(r'create_project$', Project_Operation.create_project),
    re_path(r'delete_project$', Project_Operation.remove_project),

    re_path(r'alter_ddl$', Project_Operation.alter_ddl),

    re_path(r'alter_presentation$', Preseation_Operation.alter_project_presentation),
    re_path(r'auto_group$', Group_Operation.auto_grouping),

    re_path(r'get_category$', Category_Operation.get_category),
    re_path(r'delete_category$', Category_Operation.delete_category),

    path('group_mark', group_mark),
    path('personal_score', personal_score),
    path('task_score', task_score),
    path('task_comment', task_comment),
    path('total_score', total_score),
    path('upload_team', upload_team),
    path('upload_person', upload_person),
    path('get_file', get_file),
    path('send_to_class', send_to_class),
    path('send_to_group', send_to_group),
    path('send_to_stu', send_to_stu),
    path('set_sa', set_sa),
    path('get_class_pro', get_class_pro),
    path('edit_temp', edit_temp),
    path('upload_mark_file', upload_mark_file),
    path('update_temp', update_temp)
]
