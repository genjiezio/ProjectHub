from django.core.cache import caches
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from django.utils import timezone
from rest_framework.views import APIView

from PHelper import settings
from padmin.visit_info import record_visit_info
from project.models import Project_Student_Group, Student_Course, Group, Student_Message, Course_Message, Project, \
    Category, Project_Label, Label
from student.models import Student, Student_Information
from student.views import generate_code


class loginView(APIView):
    def post(self, request):
        response = {}
        session_cache = caches['s_session']
        try:
            post_content = request.data
            account = post_content["name"]
            password = post_content["password"]
            student = Student.objects.filter(account=account)
            if not student:
                response['msg'] = 'Account not exits!'
                response['status'] = 1000
                return JsonResponse(response)
            student = student[0]
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
                response['sessionid'] = sessionid
                session_cache.set(key=student.account, value=sessionid,
                                  timeout=request.session.get_expiry_age())
            else:
                response['msg'] = 'Password wrong!'
                response['status'] = 1000
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class logoutView(APIView):
    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content['account']
            session_cache = caches['s_session']
            session_cache.delete(key=account)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class verifyView(APIView):
    def post(self, request):
        response = {}

        code_cache = caches['default']
        try:
            post_content = request.data
            email = post_content['email']
            code = generate_code()
            email_from = settings.EMAIL_HOST_USER
            title = "PHelper Account Registration Notice"
            msg = 'Please keep the verification code confidential if it is not operated by you.\n ' + \
                  'Verification code (6 effective eff): ' + code
            send_mail(title,
                      msg,
                      email_from,
                      [email])
            code_cache.set(email, code, 300)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class createView(APIView):
    def post(self, request):
        response = {}
        code_cache = caches['default']
        try:
            post_content = request.data
            account = post_content['name']
            email = post_content['email']
            password = post_content['password']
            code = post_content['code']
            data = code_cache.get(email)

            student = Student.objects.filter(account=account)

            if student:
                response['msg'] = 'Account already exists.'
                response['status'] = 400
            elif data and data == code:
                student = Student.objects.create(account=account, email=email, password=password)
                student.save()
                student_information=Student_Information.objects.create(name=account,student=student)
                student_information.save()
                response['msg'] = 'success'
                response['status'] = 200
                code_cache.delete(key=email)
            else:
                response['msg'] = 'code error'
                response['status'] = 400

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class getProjectView(APIView):
    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            student = Student.objects.get(account=account)
            course_list = student.course_set.filter(terminate=False)
            response['course'] = []
            for course in course_list:
                course_info = {}
                course_info['course_id'] = course.id
                course_info['course_name'] = course.name
                course_info['course_project'] = {}
                project_todos_info = []
                project_dones_info = []
                project_todos = course.project_set.filter(deadline__gte=timezone.now())
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

                course_info['course_project'] = project_todos_info

                student_course = Student_Course.objects.filter(student=student, course=course)
                if student_course:
                    student_course=student_course[0]
                if student_course.character == 'STU':
                    response['course'].append(course_info)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)


class checkGroupView(APIView):
    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            student = Student.objects.get(account=account)
            project_id = post_content["project_id"]
            project_student_group = Project_Student_Group.objects.filter(student_id=student.id, project_id=project_id)

            group_info = {}
            group_info['group_id'] = -1
            if project_student_group:
                project_student_group = project_student_group[0]
                group_info['group_id'] = project_student_group.group.id
                group_info['name'] = project_student_group.group.name
            response['group'] = group_info
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)


class getGroupPageView(APIView):

    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            student = Student.objects.get(account=account)
            project_id = post_content['project_id']
            group_list = Group.objects.filter(project_id=project_id)
            response['groupList'] = []
            for group in group_list:
                group_info = {}
                group_info['group_id'] = group.id
                group_info['group_name'] = group.name
                group_info['group_member'] = []
                skill = set()
                project_student_group_list = Project_Student_Group.objects.filter(group=group, project=group.project)
                for project_student_group in project_student_group_list:
                    member = project_student_group.student
                    group_info['group_member'].append(member.student_information.name)
                    project_label_list = member.project_label_set.all()
                    for project_label in project_label_list:
                        skill.add(project_label.label.name)
                group_info['group_skill'] = list(skill)
                response['groupList'].append(group_info)
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class getMyGroupView(APIView):

    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            student = Student.objects.get(account=account)
            group_id = post_content['group_id']
            group = Group.objects.filter(id=group_id)
            response['project_info'] = {}
            response['group_info'] = {}
            response['messageList'] = []
            response['groupGrade'] = 0
            response['personalGrade'] = 0

            if group:
                group = group[0]
                response['project_info']['project_class'] = group.project.course.name
                response['project_info']['project_name'] = group.project.name
                response['project_info']['project_deadline'] = group.project.deadline.strftime('%Y-%m-%d : %H:%M')
                response['group_info']['group_name'] = group.name
                member_list = []
                project_student_group_list = Project_Student_Group.objects.filter(project=group.project, group=group)
                for project_student_group in project_student_group_list:
                    member_list.append(project_student_group.student.student_information.name)
                response['group_info']['group_member'] = " ".join(str(member) for member in member_list)
                project_message_list = Course_Message.objects.filter(course=group.project.course)
                for i, project_message in enumerate(project_message_list):
                    response['messageList'].append({'project_index': i, 'project_message': project_message.content})
                response['groupGrade'] = group.grade
                project_student_group = Project_Student_Group.objects.filter(project=group.project, group=group,
                                                                             student=student)
                if project_student_group:
                    project_student_group = project_student_group[0]
                    response['personalGrade'] = project_student_group.grade

            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)


class joinGroupView(APIView):
    def post(self, request):
        response = {}
        post_content = request.data
        account = post_content["account"]
        student = Student.objects.get(account=account)
        group_id = post_content['group_id']
        group = Group.objects.get(id=group_id)
        if not group:
            return JsonResponse({'status': 1000, 'msg': 'No Group'})
        project_id = group.project.id
        project_student_group = Project_Student_Group.objects.filter(project_id=project_id, student=student)

        if project_student_group:
            response['msg'] = 'You have already joined a team'
            response['status'] = 300
        else:
            group = Group.objects.get(id=group_id)
            project = group.project
            group_course = Student_Course.objects.filter(student=group.captain, course=project.course)

            student_course = Student_Course.objects.filter(student_id=student.id, course=project.course)
            if student_course and group_course:
                student_course = student_course[0]
                group_course = group_course[0]
                if student_course.character=='SA':
                    response['msg'] = 'SA不能组队'
                    response['status'] = 1000
                elif project.across or student_course.lab == group_course.lab:
                    message = 'Apply to join'
                    self.send_to_stu(project_id, group_id, student.id, message)
                    response['msg'] = '正在申请'
                    response['status'] = 200
                else:
                    response['msg'] = '无法跨班组队'
                    response['status'] = 300
        return JsonResponse(response)

    def send_to_stu(self, project_id, group_id, sid, join_reason):
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


class getMessageView(APIView):

    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            print(account)
            student = Student.objects.get(account=account)
            message_list = Student_Message.objects.filter(student=student, read=False)
            response['messageList'] = []
            for message in message_list:
                message_info = {}
                message_info['course_id'] = message.message.course.id
                message_info['message_id'] = message.message.id
                message_info['sender'] = message.message.sender
                message_info['project_class'] = message.message.course.name
                message_info['project_message'] = message.message.content

                response['messageList'].append(message_info)
            response['msg'] = 'success'
            response['status'] = 200

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)


class readMessageView(APIView):

    def post(self, request):
        response = {}
        try:
            post_content = request.data
            account = post_content["account"]
            message_id = post_content["message_id"]
            student = Student.objects.get(account=account)
            student_message = Student_Message.objects.filter(message_id=message_id)
            if student_message:
                student_message = student_message[0]
                student_message.read = True
                student_message.save()
            message_list = Student_Message.objects.filter(student=student, read=False)
            response['messageList'] = []
            for message in message_list:
                message_info = {}
                message_info['course_id'] = message.message.course.id
                message_info['message_id'] = message.message.id
                message_info['sender'] = message.message.sender
                message_info['project_class'] = message.message.course.name
                message_info['project_message'] = message.message.content

                response['messageList'].append(message_info)
            response['msg'] = 'success'
            response['status'] = 200

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)
