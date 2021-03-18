import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from project.models import Student_Message, Group, Project_Student_Group
from student.models import Student_Information, Student


@require_http_methods(["POST"])
def edit_user(request):
    post_content = json.loads(request.body, encoding='utf-8')
    sid = post_content['sid']
    user = post_content['user']
    basic = post_content['basic']
    student_info = Student_Information.objects.get(student=sid)
    student = Student.objects.get(id=sid)
    if not student or not student_info:
        return JsonResponse({'status': 1000, 'msg': 'Student Not Found!'})
    student.email = user['mail']
    student.save()
    student_info.name = user['name']
    student_info.grade = user['grade']
    student_info.sex = basic['sex']
    student_info.education = basic['edu']
    student_info.school = basic['school']
    student_info.major = basic['major']
    student_info.description = basic['desc']
    student_info.save()
    response = {'status': 200, 'msg': 'Update Successfully!', 'user': user, 'basic': basic}
    return JsonResponse(response)


@require_http_methods(["POST"])
def get_info_user(request):
    response = {}
    post_content = json.loads(request.body, encoding='utf-8')
    sid = post_content['sid']
    student_info = Student_Information.objects.get(student=sid)
    student = Student.objects.get(id=sid)
    response['user'] = {'name': student_info.name, 'grade': student_info.grade, 'mail': student.email}
    response['basic'] = {'sex': student_info.sex, 'edu': student_info.education,
                         'school': student_info.school, 'major': student_info.major,
                         'desc': student_info.description}
    return JsonResponse(response)


@require_http_methods(["POST"])
def get_message(request):
    def take_date(elem):
        return elem['date']

    msgs = []
    post_content = json.loads(request.body, encoding='utf-8')
    sid = post_content['sid']
    msgList = Student_Message.objects.filter(student_id=sid, read=False)
    for msg in msgList:
        m = {'mid': msg.id, 'sender': msg.message.sender, 'date': msg.message.send_time,
             'content': msg.message.content, 'project': msg.message.course.name,
             'needConfirm': msg.needConfirm, 'isConfirm': msg.accepted}
        msgs.append(m)
    msgs.sort(key=take_date, reverse=True)
    return JsonResponse({'msgs': msgs})


def confirm_msg(request):
    def is_request(content):
        return content.startswith('From')

    def edit_group(group, student):
        maxsize = group.project.group_maxsize
        if group.number == maxsize:
            return False
        group.number += 1
        group.save()
        set_into_group = Project_Student_Group(project=group.project, student_id=student, group=group)
        set_into_group.save()
        return True

    post_content = json.loads(request.body, encoding='utf-8')
    mid = post_content['mid']
    accepted = post_content['accepted']
    msg = Student_Message.objects.get(id=mid)
    if is_request(msg.message.content) and accepted:
        g = Group.objects.get(id=msg.secretMsg)
        stu = msg.message.sender
        if not edit_group(g, stu):
            return JsonResponse({'status': 1000, 'msg': 'Group is Full'})
    msg.accepted = accepted
    msg.read = True
    msg.save()
    return JsonResponse({'status': 200, 'msg': 'ok'})


def delete_msg(request):
    post_content = json.loads(request.body, encoding='utf-8')
    mid = post_content['mid']
    sid = post_content['sid']
    msg = Student_Message.objects.get(id=mid)
    msg.read = True
    msgList = Student_Message.objects.filter(student_id=sid, read=False)
    msgs, response = [], {}
    for msg in msgList:
        m = {'mid': msg.id, 'sender': msg.message.sender, 'date': msg.message.send_time,
             'content': msg.message.content, 'project': msg.message.course.name,
             'needConfirm': msg.needConfirm, 'isConfirm': msg.accepted}
        msgs.append(m)
    print(msgs)
    response['msgs'] = msgs
    response['status'] = 200
    response['msg'] = 'ok'
    return JsonResponse(response)

