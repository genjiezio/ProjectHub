import hashlib
import os
import uuid

import datetime
from random import randint

from django.core.cache import caches
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
import json

from PHelper import settings
from project.models import Student_Message, Course_Message, Project_Category, Category, Group_Desire_Label, Project, \
    Project_Relation
from student.models import Student, Student_Information
from project.models import Student_Course, Group, Project_Student_Group, Label, Project_Label, Student_Label
from padmin.visit_info import record_visit_info


class Relogin():
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            session_cache = caches['s_session']
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


def generate_code():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(uuid_str)
    code_str = md5.hexdigest()
    code = ''
    for i in range(6):
        code += code_str[randint(0, len(code_str) - 1)]
    return code


class Account_Operation():

    @require_http_methods(["POST"])
    def verify(request):
        response = {}
        code_cache = caches['default']
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            email = post_content['email']
            code = generate_code()
            email_from = settings.EMAIL_HOST_USER
            title = "PHelper Account Registration Notice"
            msg = 'Please keep the verification code confidential if it is not operated by you.\n ' + \
                  'Verification code (5 effective eff): ' + code
            send_mail(title,
                      msg,
                      email_from,
                      [email])
            code_cache.set(code, email, 300)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
            print(str(e))
        return JsonResponse(response)


    @require_http_methods(["POST"])
    def create_account(request):
        response = {}
        code_cache = caches['default']
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            account = post_content['name']
            email = post_content['email']
            password = post_content['password']
            code = post_content['code']
            data = code_cache.get(code)
            if data and data == email:
                student = Student.objects.create(account=account, email=email, password=password)
                student.save()
                si = Student_Information(student=student)
                si.name = student.account
                si.save()
                response['msg'] = 'success'
                response['status'] = 200
            else:
                response['msg'] = 'code error'
                response['status'] = 400

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)

    @require_http_methods(["POST"])
    def find_account(request):
        response = {}
        print(response)
        code_cache = caches['default']
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            account = post_content['name']
            email = post_content['email']
            password = post_content['password']
            code = post_content['code']
            data = code_cache.get(code)
            if data and data == email:
                student = Student.objects.create(account=account, email=email, password=password)
                student.save()
                si = Student_Information(student=student)
                si.name = student.account
                si.save()
                response['msg'] = 'success'
                response['status'] = 200
            else:
                response['msg'] = 'code error'
                response['status'] = 400

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)

    @csrf_exempt
    @require_http_methods(["POST"])
    def check_account(request):
        response = {}
        session_cache = caches['s_session']
        if request.method == 'POST':
            try:
                post_content = json.loads(request.body, encoding='utf-8')
                account = post_content["name"]
                password = post_content["password"]
                student = Student.objects.get(account=account)

                if check_password(password, student.password):
                    record_visit_info(request, account, 'student')
                    data = session_cache.get(student.account)
                    request.session.set_expiry(0)
                    request.session['account'] = student.account
                    request.session['is_login'] = True
                    sessionid = request.session.session_key
                    if data and data != sessionid:
                        response['msg'] = 'Warning: Your account is already logged in elsewhere.'
                        response['status'] = 207
                    else:
                        response['msg'] = 'success'
                        response['status'] = 200
                    response['sid'] = student.id
                    session_cache.set(key=student.account, value=sessionid,
                                      timeout=request.session.get_expiry_age())


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
            session_cache = caches['s_session']
            session_cache.delete(key=account)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class Homepage():

    def get_pro_info(project_list, sid):
        project_list_info = []
        calend_info = []
        for project in project_list:
            deadline_info = {}
            project_info = {}
            deadline_info['months'] = [str('%02d' % project.deadline.month)]
            deadline_info['days'] = [str('%02d' % project.deadline.day)]
            deadline_info['things'] = project.name
            deadline_info['time'] = project.deadline.strftime('%H:%M')
            calend_info.append(deadline_info)
            project_info['id'] = project.id
            project_info['title'] = project.name
            project_info['class'] = project.course.name
            project_info['lab'] = 0
            project_info['SA'] = False
            student_course = Student_Course.objects.filter(student_id=sid, course=project.course)
            project_student_group = Project_Student_Group.objects.filter(project=project, student_id=sid)
            project_info['groupid'] = -1
            if project_student_group:
                project_info['id'] = project_student_group[0].group.id
                project_info['groupid'] = project_student_group[0].group.id
            if student_course:
                project_info['lab'] = student_course[0].lab
                project_info['SA'] = (student_course[0].character == 'SA')
            project_list_info.append(project_info)
            print(project_list_info)
        return project_list_info, calend_info

    @Relogin
    def get_homepage(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])

            student = Student.objects.get(id=sid)
            response['msg'] = student.account
            course_list = student.course_set.filter(terminate=False)
            response['classes'] = []
            response['todos'] = []
            response['dones'] = []
            response['prodata'] = []
            response['calendarData'] = []

            for course in course_list:
                course_info = {}
                course_info['id'] = course.id
                course_info['title'] = course.name
                response['classes'].append(course_info)
                project_todos = course.project_set.filter(deadline__gt=timezone.now())
                project_dones = course.project_set.filter(deadline__lte=timezone.now())

                project_todos_list_info, calend_todos_info = Homepage.get_pro_info(project_todos, sid)
                for project_todos in project_todos_list_info:
                    if project_todos['groupid'] == -1:
                        response['prodata'].append(project_todos)
                    else:
                        response['todos'].append(project_todos)
                response['calendarData'].extend(calend_todos_info)
                project_dones_list_info, calend_dones_info = Homepage.get_pro_info(project_dones, sid)
                response['dones'].extend(project_dones_list_info)
                response['calendarData'].extend(calend_dones_info)
            student_message_list = Student_Message.objects.filter(student_id=sid, read=False)
            response['msg2'] = []
            for student_message in student_message_list:
                response['msg2'].append(student_message.message.content)

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)

    @Relogin
    def get_terminal_project(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)

            course_list = student.course_set.filter(terminate=True)

            response['project'] = []
            for course in course_list:

                project_list = course.project_set.filter(deadline__lte=timezone.now())

                for project in project_list:
                    project_info = {}
                    project_info['name'] = project.name
                    project_info['time'] = project.deadline.strftime('%Y-%m-%d')
                    project_student_group = Project_Student_Group.objects.get(project=project, student=student)
                    project_info['grade'] = project_student_group.grade

                    response['project'].append(project_info)

        except Exception as e:
            print(e)
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)


class Course_Operation():
    @Relogin
    @require_http_methods(["POST"])
    def get_course(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            course_all = student.course_set.all()
            response['course'] = json.loads(serializers.serialize("json", course_all))
            response['msg'] = 'success'
            response['error_num'] = 0
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def get_project(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            course_list = student.course_set.filter(terminate=False)
            response['course'] = []
            for course in course_list:
                course_info = {}
                course_info['course_id'] = course.id
                course_info['course_name'] = course.name
                course_info['course_project'] = {}
                project_todos_info = []
                project_dones_info = []
                project_todos = course.project_set.filter(deadline__gt=timezone.now())
                project_dones = course.project_set.filter(deadline__lte=timezone.now())
                for project in project_todos:
                    project_info = {}
                    project_info['project_id'] = project.id
                    project_info['project_name'] = project.name
                    project_info['project_start'] = project.start
                    project_info['project_deadline'] = project.deadline
                    project_info['project_description'] = project.description
                    project_info['project_group_maxsize'] = project.group_maxsize
                    project_info['project_group_minsize'] = project.group_minsize
                    project_info['index'] = project.index
                    project_todos_info.append(project_info)

                for project in project_dones:
                    project_info = {}
                    project_info['project_id'] = project.id
                    project_info['project_name'] = project.name
                    project_info['project_start'] = project.start
                    project_info['project_deadline'] = project.deadline
                    project_info['project_description'] = project.description
                    project_info['project_group_maxsize'] = project.group_maxsize
                    project_info['project_group_minsize'] = project.group_minsize
                    project_info['index'] = project.index
                    project_dones_info.append(project_info)

                course_info['course_project']['todos'] = project_todos_info
                course_info['course_project']['does'] = project_dones_info

                student_course = Student_Course.objects.get(student=student, course=course)
                if student_course.character == 'SA':
                    response['course_SA'].append(course_info)
                elif student_course.character == 'STU':
                    response['course_STU'].append(course_info)
                response['course'].append(course_info)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000



class Label_Operation():
    @Relogin
    def add_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            input_value = str(post_content["str"]).split(':')
            label_name = input_value[0]
            label_proficiency = int(input_value[1])
            label = Label.objects.filter(name=label_name)

            if not label:
                label = Label.objects.create(name=label_name)
                label.save()
            else:
                label = label[0]
            student_label = Student_Label.objects.filter(student=student, label=label)

            if student_label:
                response['msg'] = 'Label exits. Please change name.'
                response['status'] = 1000
            else:
                student_label = Student_Label.objects.create(student=student, label=label,
                                                             proficiency=label_proficiency)
                student_label.save()
                return Label_Operation.get_label(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def get_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')

            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            student_label_list = Student_Label.objects.filter(student=student)
            response['skill'] = {}
            for student_label in student_label_list:
                proficiency = student_label.proficiency
                name = student_label.label.name
                response['skill'][name] = proficiency
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def remove_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            label_name = post_content["skill"]
            student_label = Student_Label.objects.filter(label__name=label_name, student=student)
            if student_label:
                student_label = student_label[0]
                student_label.delete()
                response['msg'] = 'success'
                response['status'] = 200
            else:
                response['msg'] = 'label not exist'
                response['status'] = 200
            return Label_Operation.get_label(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def add_project_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            student = Student.objects.get(id=sid)
            label_name = post_content["label_name"]
            category_id = int(post_content["category_id"])
            project_id = int(post_content["project_id"])
            label = Label.objects.filter(name=label_name)
            if label:
                label = label[0]
            else:
                label = Label.objects.create(name=label_name)

            project_label = Project_Label.objects.create(student_id=sid, label=label, category_id=category_id,
                                                         project_id=project_id)
            project_label.save()
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def get_project_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            project_id = int(post_content["project_id"])
            project_label_list = Project_Label.objects.filter(student_id=sid, project_id=project_id)
            response['student_label'] = []
            for project_label in project_label_list:
                project_label_info = {}
                project_label_info['label_id'] = project_label.label.id
                project_label_info['label_name'] = project_label.label.name
                response['student_label'].append(project_label_info)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
    @Relogin
    def remove_project_label(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            project_id = int(post_content["project_id"])
            label_id = int(post_content["label_id"])
            project_label = Project_Label.objects.filter(project_id=project_id, student_id=sid, label_id=label_id)
            if project_label:
                project_label[0].delete()
                response['msg'] = 'success'
                response['status'] = 200
            else:
                response['msg'] = 'label not exist'
                response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)

    def get_stuent_project_label(sid, project_id):
        stuent_project_label = []
        try:
            project_label_list = Project_Label.objects.filter(student_id=sid, project_id=project_id)
            for project_label in project_label_list:
                stuent_project_label.append(project_label.label.name)
        except Exception as e:
            raise e
        return JsonResponse(stuent_project_label)


class Group_Operation():
    def get_group_memberinfo(group_id, project_id):
        group_member = []
        group_leader = {}
        tech_set = set()

        project_student_group_list = Project_Student_Group.objects.filter(group_id=group_id, project_id=project_id)
        for project_student_group in project_student_group_list:

            member = project_student_group.student

            member_info = {}
            member_info['id'] = member.id
            member_info['name'] = member.student_information.name
            member_info['job'] = []
            member_info['lab'] = 0
            student_course = Student_Course.objects.filter(course=project_student_group.project.course, student=member)
            if student_course:
                member_info['lab'] = student_course[0].lab
            job = set()
            member_label_list = Project_Label.objects.filter(student=member, project_id=project_id)
            for member_label in member_label_list:
                job.add(member_label.category.name)
                tech_set.add(member_label.label.name)
            member_info['job'] = ", ".join(str(j) for j in list(job))
            if project_student_group.group.captain == member:
                group_leader = member_info
            else:
                group_member.append(member_info)

        return group_leader, group_member, list(tech_set)
    @csrf_exempt
    @Relogin
    def get_project_group(request):
        response = {}
        try:

            post_content = json.loads(request.body, encoding='utf-8')
            project_id = int(post_content['pid'])
            group_list = Group.objects.filter(project_id=project_id)

            response['tableData'] = []
            for group in group_list:
                group_info = {}
                group_info['id'] = group.id
                group_info['name'] = group.name

                student_course = Student_Course.objects.filter(student=group.captain, course=group.project.course)

                group_info['lab'] = 0

                if student_course:
                    group_info['lab'] = student_course[0].lab

                group_info['desc'] = group.description
                group_leader, group_member, tech = Group_Operation.get_group_memberinfo(group.id, project_id)
                group_info['tech'] = tech
                group_info['memb'] = group_member
                group_info['leader'] = group_leader
                response['tableData'].append(group_info)

            response['proCate'] = []
            project_category_list = Project_Category.objects.filter(project_id=project_id)

            for project_category in project_category_list:
                project_category_info = {}
                project_category_info['value'] = project_category.category.id
                project_category_info['label'] = project_category.category.name
                response['proCate'].append(project_category_info)
            response['msg'] = "Success"
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)
    @Relogin
    def create_group(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            sid = int(post_content["sid"])
            print(sid)
            student = Student.objects.get(id=sid)
            project_id = int(post_content['pid'])
            group_name = post_content['addTeam']['name']
            group_desc = post_content['addTeam']['desc']
            group_project_label_list = str(post_content['addTeam']['tech']).split(',')
            group_project_category = int(post_content['addTeam']['category'])
            isAccept = bool(post_content['addTeam']['isAccept'])
            isNew = bool(post_content['addTeam']['isNew'])
            group_desire_label_list = str(post_content['addTeam']['desiTech']).split(',')

            project_student_group = Project_Student_Group.objects.filter(student=student, project_id=project_id)

            if project_student_group:
                response['msg'] = "You already have a group."
                response['status'] = 1000
            else:
                category = Category.objects.get(id=group_project_category)
                for group_project_label in group_project_label_list:
                    group_label = Label.objects.filter(name=group_project_label)
                    if group_label:
                        group_label = group_label[0]
                    else:
                        group_label = Label.objects.create(name=group_project_label)
                        group_label.save()

                        project_label = Project_Label.objects.update_or_create(student=student, label=group_label,
                                                                               category_id=group_project_category,
                                                                               project_id=project_id)
                        project_label[0].save()
                if not isAccept or isNew:
                    group = Group.objects.create(name=group_name, description=group_desc, project_id=project_id,
                                                 number=1, captain=student)
                    group.save()
                    project_student_group = Project_Student_Group.objects.create(student=student, project_id=project_id,
                                                                                 group=group)
                    project_student_group.save()
                    for label in group_desire_label_list:
                        desire_label = Label.objects.filter(name=label)
                        if desire_label:
                            desire_label = desire_label[0]
                        else:
                            desire_label = Label.objects.create(name=label)

                        group_desire_label = Group_Desire_Label.objects.create(label=desire_label, group=group)
                        group_desire_label.save()
                else:
                    title = 'Team Finding'
                    content = 'Account: ' + student.account + '; \n' + 'Name: ' + \
                              student.student_information.name + '; \n' + 'Direction: ' + category.name + \
                              '( ' + project_label.label.name + ' )'
                    # project_message = Project_Message.objects.create(title=title, content=content,
                    #                                                  project_id=project_id)
                    # 发送邮件
                    project_student_group_list = Project_Student_Group.objects.filter(project_id=project_id)
                    # for project_student_group in project_student_group_list:
                    # student_message = Student_Message.objects.create(message=project_message,
                    #                                                  student=project_student_group.group.captain)
                    # student_message.save()
                return Group_Operation.get_project_group(request)
        except Exception as e:
            raise e
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)
    @Relogin
    def join_group(request):
        response = {}

        post_content = json.loads(request.body, encoding='utf-8')
        sid = post_content["sid"]
        student = Student.objects.get(id=sid)
        project_id = post_content['pid']
        group_id = post_content['gid']
        group_project_label_list = str(post_content['info']['tech']).split(',')
        group_project_category = int(post_content['info']['job'])
        join_reason = str(post_content['info']['desc'])
        project_relation = Project_Relation.objects.filter(project_id=project_id)
        index = -1
        if project_relation:
            index = project_relation[0].index

        project_student_group = Project_Student_Group.objects.filter(student=student,
                                                                     project__project_relation__index=index)
        if project_student_group:
            response['msg'] = 'You have already joined a team'
            response['status'] = 300
        else:
            group = Group.objects.get(id=group_id)
            project = group.project
            group_course = Student_Course.objects.filter(student=group.captain, course=project.course)

            student_course = Student_Course.objects.filter(student_id=sid, course=project.course)
            if student_course and group_course:
                student_course = student_course[0]
                group_course = group_course[0]
                if student_course.character == 'SA':
                    print(student_course.character)
                    print(student_course.id)

                    response['msg'] = 'SA不能组队'
                    response['status'] = 1000
                elif project.across or student_course.lab == group_course.lab:

                    for group_project_label in group_project_label_list:
                        label = Label.objects.filter(name=group_project_label)
                        if label:
                            label = label[0]
                        else:
                            label = Label.objects.create(name=group_project_label)
                            label.save()
                        project_label = Project_Label.objects.filter(student_id=sid, label=label, project=project,
                                                                     category_id=group_project_category)
                        if not project_label:
                            project_label = Project_Label.objects.create(student_id=sid, label=label,
                                                                         project=project,
                                                                         category_id=group_project_category)
                            project_label.save()
                    message = 'Direction: ' + Category.objects.get(id=group_project_category).name + '\n' + \
                              'Skill (want use): ' + post_content['info']['tech'] + '\n' + join_reason

                    Group_Operation.send_to_stu(project_id, group_id, sid, message)
                    response['msg'] = '正在申请'
                    response['status'] = 200
                else:
                    response['msg'] = '无法跨班组队'
                    response['status'] = 300
        return JsonResponse(response)

    def send_to_stu(project_id, group_id, sid, join_reason):
        sender = sid
        groupID = group_id
        classID = Project.objects.get(id=project_id).course.id
        student = Student.objects.get(id=sender)
        group = Group.objects.get(id=groupID)
        content = 'From {}:\n\t reason: {}' \
            .format(student.student_information.name, join_reason)
        sendtime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        message = Course_Message(course_id=classID, sender=sender, sender_character='stu',
                                 send_time=sendtime, content=content)
        message.save()
        leader = Group.objects.get(id=groupID).captain.id
        sm = Student_Message(student_id=leader, message=message, needConfirm=True, secretMsg=groupID)
        sm.save()
