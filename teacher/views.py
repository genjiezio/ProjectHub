from django.core.mail import send_mail
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from PHelper import settings
from project.models import Group, Group_Grades, Project_Student_Group, Group_File, Student_Message, \
    Project, Course, Course_Message, Student_Course, Teacher_Course, Project_MarkSheet
from student.models import Student_Information
from teacher.account_view import Relogin

# Create your views here.
@Relogin
def group_mark(request):
    response = {}
    studentID = request.GET.get('studentId')
    teacherID = request.GET.get('teacherId')
    groupid = request.GET.get('id')
    if not Group.objects.filter(id=groupid):
        return JsonResponse({'status': 999, 'msg': 'GroupNotExist'})
    group = Group.objects.get(id=groupid)
    if (studentID and teacherID) or (not studentID and not teacherID):
        return JsonResponse({'status': 1000, 'msg': 'NoAccessAuthorization'})
    elif studentID:
        is_sa = Student_Course.objects.get(student_id=studentID, course=group.project.course)
        if not is_sa.character == 'SA':
            return JsonResponse({'status': 1001, 'msg': 'StudentNoAccessAuthorization'})
    elif teacherID and not Teacher_Course.objects.filter(teacher=teacherID, course=group.project.course):
        return JsonResponse({'status': 1002, 'msg': 'TeacherNoAccessAuthorization'})
    group_mark = Group_Grades.objects.filter(group=groupid)
    list0 = []
    idnum = 1
    for gm in group_mark:
        list0.append({'id': idnum, 'name': gm.markSheet.name, 'getScore': gm.grade,
                      'fullScore': gm.markSheet.proportion, 'text': gm.comment, 'key': gm.id})
        idnum += 1
    response['teamScores'] = list0
    list1 = []
    group_student = Project_Student_Group.objects.filter(group=groupid)
    idnum = 1
    for stu in group_student:
        stu_info = Student_Information.objects.get(student=stu.student.id)
        list1.append({'id': idnum, 'name': stu_info.name, 'score': stu.grade, 'key': stu.id})
        idnum += 1
    response['personalScore'] = list1
    filelist = []
    groupFiles = Group_File.objects.filter(group_id=groupid)
    for file in groupFiles:
        filelist.append([file.file_name, file.id])
    response['fileList'] = filelist
    response['status'] = 200
    return JsonResponse(response)


@require_http_methods(["POST"])
@Relogin
def personal_score(request):
    post_content = json.loads(request.body, encoding='utf-8')
    key = post_content['key']
    score = post_content['score']
    person_mark = Project_Student_Group.objects.get(id=key)
    if person_mark:
        person_mark.grade = score
        person_mark.save()
        return JsonResponse({'msg': 'ok', 'status': 200})
    else:
        return JsonResponse({'msg': 'fail', 'status': 1000})



@require_http_methods(["POST"])
@Relogin
def task_score(request):
    post_content = json.loads(request.body, encoding='utf-8')
    key = post_content['key']
    score = post_content['getScore']
    group_mark = Group_Grades.objects.get(id=key)
    if group_mark:
        group_mark.grade = score
        group_mark.save()
        return JsonResponse({'msg': 'ok', 'status': 200})
    else:
        return JsonResponse({'msg': 'fail', 'status': 1000})


@require_http_methods(["POST"])
@Relogin
def task_comment(request):
    post_content = json.loads(request.body, encoding='utf-8')
    key = post_content['key']
    comment = post_content['comment']
    group_mark = Group_Grades.objects.get(id=key)
    if group_mark:
        group_mark.comment = comment
        group_mark.save()
        return JsonResponse({'msg': 'ok', 'status': 200})
    else:
        return JsonResponse({'msg': 'fail', 'status': 1000})


@require_http_methods(["POST"])
@Relogin
def total_score(request):
    post_content = json.loads(request.body, encoding='utf-8')
    key = post_content['id']
    score = post_content['totalScore']
    group = Group.objects.get(id=key)
    if group:
        group.grade = score
        group.save()
        return JsonResponse({'msg': 'ok', 'status': 200})
    else:
        return JsonResponse({'msg': 'fail', 'status': 1000})


@csrf_exempt
def upload_team(request):
    response = {}
    key = request.POST['key']
    file = request.FILES.get("file", None)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    msg = []
    try:
        if not file.name.endswith('.csv'):
            return JsonResponse({'status': 1001, 'msg': ['FileNotCSV']})
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\r\n")
        for line in lines:
            try:
                data = line.split(",")
                if len(data) != 4:
                    return JsonResponse({'status': 1002, 'msg': ['WrongFormat']})
                task_name = data[0]
                group_mark = Group_Grades.objects.get(group=key, markSheet__name=task_name)
                if group_mark:
                    group_mark.grade = data[1]
                    group_mark.markSheet.proportion = data[2]
                    group_mark.comment = data[3]
                    group_mark.save()
                else:
                    return JsonResponse({'status': 1003, 'msg': ['WrongInformation']})
            except Exception as e:
                msg.append([line, str(e)])
        response['msg'] = msg
    except AttributeError:
        msg.append(str(AttributeError))
    if msg:
        response['msg'] = msg
        response['status'] = 1004
    else:
        response['msg'] = ['ok']
        response['status'] = 200
    print(response)
    return JsonResponse(response)


@csrf_exempt
def upload_person(request):
    key = request.POST['key']
    file = request.FILES.get("file", None)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    msg, response = [], {}
    try:
        if not file.name.endswith('.csv'):
            return JsonResponse({'status': 1001, 'msg': ['FileNotCSV']})
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\r\n")
        for line in lines:
            try:
                data = line.split(",")
                if len(data) != 2:
                    return JsonResponse({'status': 1002, 'msg': ['WrongFormat']})
                group_student = Project_Student_Group.objects.filter(group=key)
                foundName = False
                sid = -1
                for stu in group_student:
                    stu_info = Student_Information.objects.get(student=stu.student.id)
                    if stu_info.name == data[0]:
                        sid = stu_info.student.id
                        foundName = True
                if foundName:
                    group_student = Project_Student_Group.objects.get(group=key, student=sid)
                    group_student.grade = data[1]
                    group_student.save()
                else:
                    return JsonResponse({'status': 1002, 'msg': ['StudentNotFound']})
            except Exception as e:
                msg.append([line, str(e)])
        response['msg'] = msg
    except AttributeError:
        msg.append(str(AttributeError))
    if msg:
        response['msg'] = msg
        response['status'] = 1004
    else:
        response['msg'] = ['ok']
        response['status'] = 200
    print(response)
    return JsonResponse(response)

@Relogin
def get_file(request):
    def file_iterator(file, chunk_size=512):
        with open(file, mode='rb+') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    fileID = request.GET.get('fileId')
    file = None
    if fileID:
        file = Group_File.objects.get(id=fileID)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    response = StreamingHttpResponse(file_iterator(file.file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file.file_name)
    return response


def send_msg_email(message, content, receiver_list):
    email_list = []
    try:
        for receiver in receiver_list:
            msg = Student_Message(student=receiver.student, message=message, needConfirm=True)
            msg.save()
            email_list.append(msg.student.email)
        email_from = settings.EMAIL_HOST_USER
        title = 'An announcement is released from Class {}'.format(message.course.name)
        send_mail(title, content, email_from, email_list)
        return True
    except Exception as e:
        return False

@Relogin
@require_http_methods(["POST"])
def send_to_class(request):
    post_content = json.loads(request.body, encoding='utf-8')
    sender = post_content['teacherid']
    classID = post_content['classid']
    content = post_content['content']
    send_time = post_content['sendtime']
    if not Course.objects.filter(id=classID):
        return JsonResponse({'status': 1000, 'msg': 'CourseNotFound'})
    message = Course_Message(course_id=classID, sender=sender,
                             sender_character='T', send_time=send_time, content=content)
    message.save()
    receiverList = Student_Course.objects.filter(course_id=classID)
    if send_msg_email(message, content, receiverList):
        return JsonResponse({'status': 200, 'msg': 'ok'})
    else:
        return JsonResponse({'status': 1000, 'msg': 'fail'})

@Relogin
@require_http_methods(["POST"])
def send_to_group(request):
    post_content = json.loads(request.body, encoding='utf-8')
    sender = post_content['teacherid']
    groupID = post_content['groupid']
    content = post_content['content']
    send_time = post_content['sendtime']
    if not Group.objects.filter(id=groupID):
        return JsonResponse({'status': 1000, 'msg': 'CourseNotFound'})
    course = Group.objects.get(id=groupID).project.course
    message = Course_Message(course=course, sender=sender,
                             sender_character='T', send_time=send_time, content=content)
    message.save()
    receiverList = Project_Student_Group.objects.filter(group_id=groupID)
    if send_msg_email(message, content, receiverList):
        return JsonResponse({'status': 200, 'msg': 'ok'})
    else:
        return JsonResponse({'status': 1000, 'msg': 'fail'})

@Relogin
@require_http_methods(["POST"])
def send_to_stu(request):
    post_content = json.loads(request.body, encoding='utf-8')
    sender = post_content['teacherid']
    classID = post_content['classid']
    stuID = post_content['stuid']
    content = post_content['content']
    sendtime = post_content['sendtime']
    message = Course_Message(course_id=classID, sender=sender, sender_character='T', send_time=sendtime, content=content)
    message.save()
    email_list = []
    try:
        for receiver in stuID:
            sm = Student_Message(student_id=receiver, message=message, needConfirm=True)
            sm.save()
            email_list.append(sm.student.email)
        email_from = settings.EMAIL_HOST_USER
        title = 'An announcement is released from Class {}'.format(message.course.name)
        send_mail(title, content, email_from, email_list)
        return JsonResponse({'status': 200, 'msg': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 1000, 'msg': 'fail'})

@Relogin
@require_http_methods(["POST"])
def set_sa(request):
    post_content = json.loads(request.body, encoding='utf-8')
    classID = post_content['classid']
    stu_list = post_content['stuid']
    operate = post_content['operate']
    for stuID in stu_list:
        if not Student_Course.objects.filter(course_id=classID, student_id=stuID):
            return JsonResponse({'status': 1000, 'msg': 'StudentNotFound'})
        sc = Student_Course.objects.get(course_id=classID, student_id=stuID)
        sc.character = operate
        sc.save()
    return JsonResponse({'status': 200, 'msg': 'ok'})

@Relogin
@require_http_methods(["POST"])
def get_class_pro(request):
    post_content = json.loads(request.body, encoding='utf-8')
    teacherID = post_content['tid']
    classes = Teacher_Course.objects.filter(teacher_id=teacherID)
    classNameList = []
    cls_pro_dict = {}
    for c in classes:
        classNameList.append(c.course.name)
        pros = Project.objects.filter(course=c.course)
        proList = []
        for project in pros:
            proList.append({'name': project.name, 'id': project.id})
        cls_pro_dict[c.course.name] = proList
    return JsonResponse({'classes': classNameList, 'pros': cls_pro_dict})

@Relogin
@require_http_methods(["POST"])
def edit_temp(request):
    post_content = json.loads(request.body, encoding='utf-8')
    teacher_id = post_content['tid']
    pro_id = post_content['proid']
    if not post_content['tableData']:
        return JsonResponse({'status': 1000, 'msg': 'NoData'})
    table_data = post_content['tableData']
    course = Project.objects.get(id=pro_id).course
    if not Teacher_Course.objects.filter(teacher_id=teacher_id, course=course):
        return JsonResponse({'status': 1001, 'msg': 'NoAccessAuthorization'})
    sheet = Project_MarkSheet.objects.filter(project_id=pro_id)
    sheet.delete()
    msg = []
    try:
        for task in table_data:
            name = task['name']
            fullScore = task['fullScore']
            desc = task['desc']
            new_task = Project_MarkSheet(name=name, proportion=fullScore, project_id=pro_id, description=desc)
            new_task.save()
            groups = Group.objects.filter(project_id=pro_id)
            for g in groups:
                group_task = Group_Grades(group=g, markSheet=new_task)
                group_task.save()
    except Exception as e:
        msg.append(str(e))
    if msg:
        return JsonResponse({'msg': msg, 'status': 1000})
    else:
        return JsonResponse({'msg': 'ok', 'status': 200})

@Relogin
@require_http_methods(["POST"])
def update_temp(request):
    post_content = json.loads(request.body, encoding='utf-8')
    pro_id = post_content['proid']
    table_data = []
    sheets = Project_MarkSheet.objects.filter(project_id=pro_id)
    for sheet in sheets:
        table_data.append({'name': sheet.name, 'fullScore': sheet.proportion, 'desc': sheet.description})
    return JsonResponse({'tableData': table_data, 'status': 200, 'msg': 'ok'})

@Relogin
@require_http_methods(["POST"])
def upload_mark_file(request):
    response = {}
    proID = request.POST['proid']
    tid = request.POST['tid']
    print(proID)
    print(tid)
    course = Project.objects.get(id=proID).course
    if not Teacher_Course.objects.filter(teacher_id=tid, course=course):
        return JsonResponse({'status': 999, 'msg': 'NoAccessAuthorization'})
    file = request.FILES.get("file", None)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    msg = []
    try:
        if not file.name.endswith('.csv'):
            return JsonResponse({'status': 1001, 'msg': ['FileNotCSV']})
        file_data = file.read().decode("utf-8")
        lines = file_data.split("\r\n")
        for line in lines:
            try:
                data = line.split(",")

                if len(data) != 3:
                    return JsonResponse({'status': 1002, 'msg': ['WrongFormat']})
                else:
                    taskname = data[0]
                    proportion = data[1]
                    desc = data[2]
                    ms = Project_MarkSheet(name=taskname, proportion=proportion, description=desc, project_id=proID)
                    ms.save()
                    groups = Group.objects.filter(project_id=proID)
                    for g in groups:
                        group_task = Group_Grades(group=g, markSheet=ms)
                        group_task.save()
            except Exception as e:
                msg.append([line, str(e)])
        response['msg'] = msg
    except AttributeError:
        msg.append(str(AttributeError))
    if msg:
        response['msg'] = msg
        response['status'] = 1004
    else:
        response['msg'] = ['ok']
        response['status'] = 200
    print(response)
    return JsonResponse(response)

