import json
import os

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import StreamingHttpResponse

from project.models import Group, Project_Student_Group, Group_File, \
    Student_Course, Presentation_Schedule, Teacher_Course, File_Log


# projectName
# className
# labName
# leaderId
# groupName
# members:[{picture:url, name:'', studentId:},{}]
# fileList:[{name,id}]
# chooseTime:[day,start,end]
# timeList:[[day,[[start,end,choose],[]]],[]]
# logs:[{sender:,fileName:,time:},{}]


def project_page(request):
    response = {}
    studentID = request.GET.get('studentId')
    teacherID = request.GET.get('teacherId')
    groupID = request.GET.get('groupId')
    if not Group.objects.filter(id=groupID):
        return JsonResponse({'status': 1003, 'msg': 'NoGroupFound'})
    group = Group.objects.get(id=groupID)
    if studentID and not Student_Course.objects.filter(student_id=studentID, course=group.project.course):
        return JsonResponse({'status': 1001, 'msg': 'StudentNoAccessAuthorization'})
    if studentID and Student_Course.objects.get(student_id=studentID, course=group.project.course).character == 'SA':
        response['SA'] = True
    else:
        response['SA'] = False
    if (studentID and teacherID) or (not studentID and not teacherID):
        return JsonResponse({'status': 1000, 'msg': 'NoAccessAuthorization'})
    elif studentID and not Project_Student_Group.objects.filter(student_id=studentID) and not response['SA']:
        return JsonResponse({'status': 1001, 'msg': 'StudentNoAccessAuthorization'})
    elif teacherID and not Teacher_Course.objects.filter(teacher=teacherID, course=group.project.course):
        return JsonResponse({'status': 1002, 'msg': 'TeacherNoAccessAuthorization'})
    # AccessAuthorization
    response['groupName'] = group.name
    response['labName'] = Student_Course.objects.get(student=group.captain, course=group.project.course).lab
    response['projectName'] = group.project.name
    response['className'] = group.project.course.name
    response['leaderId'] = group.captain_id
    response['groupScore'] = group.grade
    if not response['SA'] and studentID and Project_Student_Group.objects.filter(student_id=studentID):
        response['personalScore'] = Project_Student_Group.objects.get(student_id=studentID, group_id=groupID).grade

    group_file = Group_File.objects.filter(group=groupID)
    fileList, logs = [], []
    for file in group_file:
        dict0 = {'id': file.id, 'name': file.file_name}
        fileList.append(dict0)
        Logs = File_Log.objects.filter(file=file)
        for log in Logs:
            dict1 = {'sender': log.op_stu.student_information.name,
                     'fileName': log.file.file_name, 'time': log.op_time, 'operation': log.operation}
            logs.append(dict1)
    response['fileList'] = fileList
    response['logs'] = logs

    student_group = group.project_student_group_set.all()
    mem = []
    for m in student_group:
        d0 = {'picture': "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png",
              'name': m.student.student_information.name, 'studentId': m.student.id}
        mem.append(d0)
    response['members'] = mem
    chooseTime = Presentation_Schedule.objects.filter(group=groupID, start__gte=timezone.now(),
                                                      project_presentation__project=group.project)
    if len(chooseTime):
        chooseTime = chooseTime[0]
        response['chooseTime'] = [chooseTime.start.strftime('%Y-%m-%d'),
                                  chooseTime.start.strftime('%H:%M'),
                                  chooseTime.end.strftime('%H:%M')]
    else:
        response['chooseTime'] = []
    timeList = Presentation_Schedule.objects.filter(start__gte=timezone.now(),
                                                    project_presentation__project=group.project)
    daylist = []
    for time in timeList:
        day = time.start.strftime('%Y-%m-%d')
        if day not in (i[0] for i in daylist):
            daylist.append([day, []])
        start = time.start.strftime('%H:%M')
        end = time.end.strftime('%H:%M')
        choose = False if not time.group else True
        for d in daylist:
            if d[0] == day:
                d[1].append([start, end, choose, time.id])
    response['timeList'] = daylist
    response['msg'] = 'ok!'
    response['status'] = 200
    return JsonResponse(response)


@csrf_exempt
def file_upload(request):
    groupID = request.POST['groupId']
    studentID = request.POST['studentId']
    file = request.FILES.get("file", None)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    if not Group.objects.filter(id=groupID):
        return JsonResponse({'status': 1001, 'msg': ['GroupNotFound']})
    group = Group.objects.get(id=groupID)
    if not group.project_student_group_set.filter(student=studentID):
        return JsonResponse({'status': 1002, 'msg': ['NoAccessAuthorization']})
    if len(file.name) > 50:
        return JsonResponse({'status': 1003, 'msg': ['FileNameTooLong']})
    msg, response = [], {}
    try:
        file_path = "D:/upload/" + str(groupID) + '/'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        if os.path.exists(file_path + file.name):
            return JsonResponse({'status': 1004, 'msg': ['SameNameFileExist']})
        destination = open(os.path.join(file_path, file.name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        group_file = Group_File(group_id=groupID, file_name=file.name,
                                file_path=file_path + file.name, student_id=studentID)
        group_file.save()
        log = File_Log(file=group_file, op_stu_id=studentID)
        log.save()
        response['fileId'] = group_file.id
    except Exception as e:
        msg.append([str(e)])
    if msg:
        response['msg'] = msg
        response['status'] = 1005
    else:
        response['msg'] = ['ok']
        response['status'] = 200
    return JsonResponse(response)


def file_download(request):
    def file_iterator(file, chunk_size=512):
        with open(file, mode='rb+') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    groupID = request.GET.get('groupId')
    studentID = request.GET.get('studentId')
    fileID = request.GET.get('fileId')
    file = None
    if fileID and studentID and groupID:
        file = Group_File.objects.get(id=fileID)
    if not file:
        return JsonResponse({'status': 1000, 'msg': ['FileNotFound']})
    group = Group.objects.get(id=groupID)
    if groupID != file.group.id and not group.project_student_group_set.filter(student=studentID):
        return JsonResponse({'status': 1001, 'msg': ['NoAccessAuthorization']})
    response = StreamingHttpResponse(file_iterator(file.file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file.file_name)
    return response


@require_http_methods(["POST"])
def file_delete(request):
    return None


@require_http_methods(["POST"])
def member_delete(request):
    post_content = json.loads(request.body, encoding='utf-8')
    groupID = post_content['groupKey']
    studentID = post_content['studentKey']
    psg = Project_Student_Group.objects.get(group_id=groupID, student_id=studentID)
    if psg:
        if str(Group.objects.get(id=groupID).captain.id) == studentID:
            studentList = Project_Student_Group.objects.filter(group_id=groupID)
            newLeader = None
            for s in studentList:
                if s.student.id != Group.objects.get(id=groupID).captain.id:
                    newLeader = s.student
                    break
            if newLeader:
                g = Group.objects.get(id=groupID)
                g.captain = newLeader
                g.save()
                psg.delete()
                return JsonResponse({'status': 1000,
                                     'msg': 'Delete Successfully!\nLeader is changed to ' +
                                            newLeader.student_information.name})
            else:
                return JsonResponse({'status': 1000,
                                     'msg': 'Please delete group LEADER!!!'})
        else:
            psg.delete()
        return JsonResponse({'status': 200, 'msg': 'Delete Successfully!'})
    else:
        return JsonResponse({'status': 1000, 'msg': 'StudentNotFound'})


@require_http_methods(["POST"])
def group_delete(request):
    post_content = json.loads(request.body, encoding='utf-8')
    groupID = post_content['groupKey']
    studentID = post_content['studentKey']
    g = Group.objects.get(id=groupID)
    if Presentation_Schedule.objects.filter(group_id=groupID):
        chooseTime = Presentation_Schedule.objects.get(group_id=groupID)
        chooseTime.group = None
        chooseTime.save()
    if str(g.captain.id) == studentID:
        g.delete()
        return JsonResponse({'status': 200, 'msg': 'Delete Successfully!'})
    else:
        return JsonResponse({'status': 1000, 'msg': 'NoAccessAuthorization'})


@require_http_methods(["POST"])
def change_group_name(request):
    post_content = json.loads(request.body, encoding='utf-8')
    groupID = post_content['groupId']
    groupName = post_content['groupName']
    group = Group.objects.get(id=groupID)
    group.name = groupName
    group.save()
    return JsonResponse({'status': 200})


@require_http_methods(["POST"])
def choose_time(request):
    post_content = json.loads(request.body, encoding='utf-8')
    timeID = post_content['timeId']
    groupID = post_content['groupId']
    new = Presentation_Schedule.objects.get(id=timeID)
    presentation_schedule = new.project_presentation
    old = Presentation_Schedule.objects.filter(group_id=groupID, project_presentation=presentation_schedule)
    for pre_time in old:
        pre_time.group = None
        pre_time.save()
    new.group_id = groupID
    new.save()
    return JsonResponse({'msg': 'ok', 'status': 200})

# def send_to_stu(project_id, group_id, sid, join_reason):
#     sender = sid
#     groupID = group_id
#     classID = Project.objects.get(id=project_id).course.id
#     student = Student.objects.get(id=sender)
#     group = Group.objects.get(id=groupID)
#     content = 'A Request to Join Your group {} from {}:\nAccount: {}\n\t{}' \
#         .format(group.name, student.student_information.name, student.account, join_reason)
#     sendtime = str(timezone.now())
#     message = Course_Message(course_id=classID, sender=sender, sender_character='stu',
#                              send_time=sendtime, content=content)
#     message.save()
#     leader = Group.objects.get(id=groupID).captain.id
#     sm = Student_Message(student_id=leader, message=message, needConfirm=True, secretMsg=groupID)
#     sm.save()
#     return JsonResponse({'status': 200, 'msg': 'ok!'})
