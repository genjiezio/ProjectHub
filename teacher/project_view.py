import csv
import datetime
import os

from django.db.models import Max
from django.utils import timezone

from django.core.cache import caches
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from student.models import Student
from teacher.models import Teacher
from project.models import Course, Project, Project_Category, Category, Project_Relation, Group, Project_Student_Group, \
    Project_Presentation, Presentation_Schedule, Student_Course


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


class Project_Operation():
    @Relogin
    def create_project(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            course_id = int(post_content["classid"])
            project_name = post_content.get("project_name")
            if not project_name:
                return JsonResponse({'status': 1000, 'msg': 'project name is null'})
            project_index = post_content.get("proindex")
            if not project_index:
                return JsonResponse({'status': 1000, 'msg': 'project index is null'})
            project_index = int(project_index)
            project_deadline = post_content.get("project_deadline")
            if not project_deadline:
                return JsonResponse({'status': 1000, 'msg': 'project deadline is null'})
            project_deadline = datetime.datetime.strptime(project_deadline, '%Y-%m-%d %H:%M:%S')
            project_group_maxsize = post_content.get("maxsize")
            if not project_group_maxsize:
                return JsonResponse({'status': 1000, 'msg': 'max size is null'})
            project_group_minsize = post_content.get("minsize")
            if not project_group_minsize:
                return JsonResponse({'status': 1000, 'msg': 'min size is null'})
            project_group_minsize = int(project_group_minsize)
            categorize = post_content.get("categorize")
            if not categorize:
                return JsonResponse({'status': 1000, 'msg': 'categorize is null'})
            categorize_list = str(categorize).split(',')

            project_presentation_time_list = post_content["prelist"]
            project_across = post_content.get("across")
            if not project_across:
                project_across = False
            else:
                project_across = bool(post_content["across"])

            project = Project.objects.filter(name=project_name, course_id=course_id)

            if project:
                response['msg'] = 'Project exits. Please change name.'
                response['status'] = 1000
                return JsonResponse(response)

            project = Project.objects.create(name=project_name, deadline=project_deadline,
                                             group_maxsize=project_group_maxsize,
                                             group_minsize=project_group_minsize, index=project_index,
                                             course_id=course_id, across=project_across)

            project.save()
            for category_name in categorize_list:
                Category_Operation.add_category(category_name, project.id)
            for presentation in project_presentation_time_list:
                if presentation['prelistid'] and presentation['timelimit']:
                    project_presentation_index = int(presentation['prelistid'])
                    project_presentation_name = '第 ' + str(project_presentation_index) + ' 次答辩'
                    project_duration = int(presentation['timelimit'])
                    project_presentation_time = presentation['tim']
                    Preseation_Operation.create_project_presentation(project_presentation_name, project.id,
                                                                     project_duration, project_presentation_index,
                                                                     project_presentation_time)
            return Teacher_Page.get_teacher_page(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)

    @Relogin
    def alter_project(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            project_id = int(post_content["project_id"])
            project_name = post_content["project_name"]
            project_index = int(post_content["index"])
            project_start = datetime.datetime.strptime(post_content["project_start"], '%Y-%m-%d %H:%M:%S')
            project_deadline = datetime.datetime.strptime(post_content["project_deadline"], '%Y-%m-%d %H:%M:%S')
            project_description = post_content["project_description"]
            project_group_maxsize = int(post_content["project_group_maxsize"])
            project_group_minsize = int(post_content["project_group_minsize"])

            project = Project.objects.filter(id=project_id)
            if not project:
                response['msg'] = 'Project not exits.'
                response['status'] = 400
            else:
                project = project[0]
                project.name = project_name
                project.start = project_start
                project.deadline = project_deadline
                project.description = project_description
                project.group_maxsize = project_group_maxsize
                project.group_minsize = project_group_minsize
                project.index = project_index
                project.save()
                response['msg'] = 'success'
                response['status'] = 200
                return Teacher_Page.get_teacher_page(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)

    @Relogin
    def alter_ddl(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            print(post_content)
            project_id = post_content.get("prokey")
            if project_id:
                project_id = int(project_id)
            else:
                return JsonResponse({'status': 1000, 'msg': 'project id is null'})

            project_deadline = post_content.get("date")
            if project_deadline:
                project_deadline = datetime.datetime.strptime(project_deadline, '%Y-%m-%d %H:%M:%S')
            else:
                return JsonResponse({'status': 1000, 'msg': 'project id is null'})
            project = Project.objects.filter(id=project_id)
            if not project:
                response['msg'] = 'project not exits'
                response['status'] = 400
            else:
                project = project[0]
                project.deadline = project_deadline
                project.save()
                response['msg'] = 'success'
                response['status'] = 200
                return Teacher_Page.get_teacher_page(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)

    @Relogin
    def remove_project(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            project_id = post_content.get("prokey")
            if project_id:
                project_id = int(project_id)
            else:
                return JsonResponse({'status': 1000, 'msg': 'project id is null'})

            project = Project.objects.filter(id=project_id)
            if not project:
                response['msg'] = 'project not exits'
                response['status'] = 400
            else:
                project = project[0]
                project.delete()
                response['msg'] = 'success'
                response['status'] = 200
                return Teacher_Page.get_teacher_page(request)
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class Teacher_Page():
    def get_course_stu_info(course):
        studentlist = []

        student_list = course.student.all()

        project_list = course.project_set.all()
        for student in student_list:
            student_info = {}
            student_info['label'] = student.student_information.name
            student_info['ikey'] = student.id
            student_info['ids'] = student.account
            isgroup = False
            for project in project_list:
                project_student_group = Project_Student_Group.objects.filter(project=project, student=student)
                if project_student_group:
                    isgroup = True
            student_info['isgroup'] = isgroup
            studentlist.append(student_info)
        return studentlist

    def get_pro_pre_info(project_id):
        prelist = []
        project_presentation_list = Project_Presentation.objects.filter(project_id=project_id).order_by('index')
        index = -1
        project_presentation_info = {}
        for project_presentation in project_presentation_list:
            project_presentation_info = {}
            project_presentation_info['presentationid'] = project_presentation.index
            project_presentation_info['presentationkey'] = project_presentation.id
            presentation_schedule_list = Presentation_Schedule.objects.filter(
                project_presentation=project_presentation).order_by('start')
            project_presentation_info['presentationname'] = project_presentation.name
            project_presentation_info['presentationtime'] = []
            if presentation_schedule_list:
                start = presentation_schedule_list[0].start
                end = presentation_schedule_list[len(presentation_schedule_list) - 1].end

                time = start.strftime('%Y-%m-%d : %H:%M') + "—" + end.strftime('%H:%M')
                project_presentation_info['presentationtime'].append(time)

                prelist.append(project_presentation_info)
        return prelist

    @Relogin
    def get_pro_group_info(course):
        prodata = []
        groupdata = []
        group_count = 0
        project_list = course.project_set.all()
        for i, project in enumerate(project_list):
            group_list = Group.objects.filter(project=project)
            for group in group_list:
                group_info = {}
                group_count += 1
                group_info['groupid'] = group_count
                group_info['pro'] = group.name
                group_info['leader'] = group.captain.student_information.name
                project_student_group_list = Project_Student_Group.objects.filter(project=project, group=group)
                member_list = []
                for project_student_group in project_student_group_list:
                    student = project_student_group.student

                    member_list.append(student.student_information.name)
                group_info['member'] = " ".join(str(member) for member in member_list)
                group_info['groupkey'] = group.id
                student_course = Student_Course.objects.filter(student=group.captain, course=group.project.course)
                group_info['lab'] = 0
                if student_course:
                    group_info['lab'] = student_course[0].lab
                groupdata.append(group_info)

            project_info = {}
            project_info['id2'] = i + 1
            project_info['pro2'] = project.name
            project_info['number'] = len(group_list)
            project_info['time'] = project.deadline.strftime('%Y-%m-%d : %H:%M')
            project_info['prelist'] = Teacher_Page.get_pro_pre_info(project.id)
            project_info['proindex'] = project.index
            project_info['prokey'] = project.id
            prodata.append(project_info)
        return prodata, groupdata

    @Relogin
    def get_teacher_page(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')

            tid = int(post_content["teacherid"])

            teacher = Teacher.objects.get(id=tid)
            course_list = teacher.course_set.filter(terminate=False, teacher_course__teacher_id=tid)
            response['class'] = []
            for course in course_list:
                course_info = {}
                course_info['id'] = course.id
                course_info['title'] = course.name
                course_info['studentlist'] = Teacher_Page.get_course_stu_info(course)
                prodata, groupdata = Teacher_Page.get_pro_group_info(course)
                course_info['prodata'] = prodata
                course_info['groupData'] = groupdata
                course_info['value'] = []
                response['class'].append(course_info)
            response['msg'] = 'success'
            response['status'] = 200

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        print(response)
        return JsonResponse(response)


class Preseation_Operation():
    def create_project_presentation(name, project_id, duration, index, time):
        try:
            if time:
                project_presentation = Project_Presentation.objects.create(name=name, project_id=project_id,
                                                                           duration=duration,
                                                                           index=index)
                project_presentation.save()

                start = datetime.datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
                end = datetime.datetime.strptime(time[1], '%Y-%m-%d %H:%M:%S')
                while start + datetime.timedelta(minutes=duration) <= end:
                    presentation_schedule = Presentation_Schedule.objects.create(start=start,
                                                                                 end=start + datetime.timedelta(
                                                                                     minutes=duration),
                                                                                 project_presentation=project_presentation)

                    presentation_schedule.save()
                    start = start + datetime.timedelta(minutes=duration)
        except Exception as e:
            pass

    @Relogin
    def alter_project_presentation(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            tid = int(post_content["teacherid"])
            project_id = int(post_content["prokey"])

            prelist = post_content["prelist"]

            project_presentation_list = Project_Presentation.objects.filter(project_id=project_id)
            for project_presentation in project_presentation_list:
                project_presentation.delete()
            for presentation in prelist:
                project_presentation_index = presentation.get('prelistid')
                project_presentation_duration = presentation.get('timelimit')
                project_presentation_time = presentation['tim']
                if project_presentation_index and project_presentation_duration and project_presentation_time:
                    project_presentation_index = int(project_presentation_index)
                    project_presentation_duration = int(project_presentation_duration)

                    project_presentation_name = '第 ' + str(project_presentation_index) + ' 次答辩'
                    Preseation_Operation.create_project_presentation(project_presentation_name, project_id,
                                                                     project_presentation_duration,
                                                                     project_presentation_index,
                                                                     project_presentation_time)
            return Teacher_Page.get_teacher_page(request)
        except Exception as e:
            response['status'] = 1000
            response['msg'] = str(e)

        return JsonResponse(response)

    @Relogin
    def remove_project_presentation(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            project_presentation_id = int(post_content["project_presentation_id"])
            project_presentation = Project_Presentation.objects.get(id=project_presentation_id)
            project_presentation.delete()
            response['msg'] = 'success'
            response['status'] = 200

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)

    @Relogin
    def remove_Presentation_Schedule(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            project_presentation_id = post_content["project_presentation_id"]
            start = datetime.datetime.strptime(post_content["start"], '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(post_content["end"], '%Y-%m-%d %H:%M:%S')
            presentation_schedule_list = Presentation_Schedule.objects.filter(start__gte=start, end__lte=end,
                                                                              project_presentation_id=project_presentation_id)
            for presentation_schedule in presentation_schedule_list:
                presentation_schedule.delete()
            response['msg'] = 'success'
            response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)


class Category_Operation():
    @Relogin
    def get_category(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            project_id = int(post_content["project_id"])
            project = Project.objects.get(id=project_id)
            if project:
                project_category_list = Project_Category.objects.filter(project_id=project_id)
                response['category'] = []
                for project_category in project_category_list:
                    category_info = {}
                    category_info['category_id'] = project_category.category_id
                    category_info['category_name'] = project_category.category.name
                    category_info['category_description'] = project_category.description
                    response['category'].append(category_info)
                response['msg'] = 'success'
                response['status'] = 200
            else:
                response['msg'] = 'Project not exists!'
                response['status'] = 1000
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

        return JsonResponse(response)

    def add_category(category_name, project_id):
        response = {}
        try:

            category = Category.objects.filter(name=category_name)
            if not category:
                category = Category.objects.create(name=category_name)
                category.save()
            else:
                category = category[0]
            project_category = Project_Category.objects.filter(project_id=project_id, category=category)
            if not project_category:
                project_category = Project_Category.objects.create(project_id=project_id, category=category)
                project_category.save()

        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000

    @Relogin
    def delete_category(request):
        response = {}
        try:
            post_content = json.loads(request.body, encoding='utf-8')
            category_id = int(post_content["category_id"])
            project_id = int(post_content["project_id"])
            project_category = Project_Category.objects.get(category_id=category_id, project_id=project_id)
            if not project_category:
                response['msg'] = 'Category not exits.'
                response['status'] = 1000
            else:
                project_category.delete()
                response['msg'] = 'success'
                response['status'] = 200
        except Exception as e:
            response['msg'] = str(e)
            response['status'] = 1000
        return JsonResponse(response)


class Group_Operation():
    @Relogin
    @Relogin
    def download_group(request):
        def file_iterator(file, chunk_size=512):
            with open(file, mode='rb+') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        try:
            course_id = request.GET.get("classid")
            course = Course.objects.get(id=course_id)
            file_path = "./group_info/"
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            file_name = course.name + "_group.csv"
            file_path = file_path + course.name + "_group.csv"
            with open(file_path, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                project_list = course.project_set.all()
                group_info = [['project', 'student_account', 'group']]
                for project in project_list:
                    project_student_group_list = project.project_student_group_set.all().order_by('project_id',
                                                                                                  'group_id')

                    for project_student_group in project_student_group_list:
                        group_info.append([project_student_group.project.name, project_student_group.student.account,
                                           project_student_group.group.name])
                writer.writerows(group_info)

            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        except Exception as e:
            return JsonResponse({'msg': str(e), 'status': 1000})
        return response
    @Relogin
    def auto_grouping(request):
        response = {}

        post_content = json.loads(request.body, encoding='utf-8')
        project_id = post_content.get("prokey")
        if project_id:
            project_id = int(project_id)
        else:
            return JsonResponse({'status': 1000, 'msg': 'project id is null'})
        project = Project.objects.get(id=project_id)

        student_list = Student.objects.filter(course=project.course, student_course__character='STU').exclude(
            project_student_group__project=project)

        group_list = Group.objects.filter(number__lt=project.group_minsize)
        project_category_list = Project_Category.objects.filter(project=project)
        pre_group_student = []
        lab_num = student_list.aggregate(Max('student_course__lab'))['student_course__lab__max']
        if not lab_num:
            lab_num = 0
        student_lab_count = []
        for i in range(lab_num):
            pre_group_student.append({-1: []})
            student_lab_count.append(0)
            for project_category in project_category_list:
                pre_group_student[i][project_category.id] = []

        for student in student_list:
            student_course = Student_Course.objects.filter(student=student, course=project.course)
            if not student_course:
                continue

            student_lab = student_course[0].lab
            student_lab_count[student_lab - 1] += 1
            student_label_list = student.project_label_set.filter(project=project)

            if student_label_list:
                pre_group_student[student_lab - 1][student_label_list[0].category.id].append(student)
            else:
                pre_group_student[student_lab - 1][-1].append(student)
        new_group_num = 0
        for i in range(lab_num):

            lab_pre_group_student = pre_group_student[i]
            key_list = list(lab_pre_group_student.keys())
            key_index = []
            for j in key_list:
                key_index.append(0)
            category_index = 0
            count = 0
            group_list_index = 0
            avg_size = int((project.group_maxsize + project.group_minsize) // 2)
            current_group = None

            while count < student_lab_count[i]:
                if category_index == len(key_list):
                    category_index = 0
                while key_index[category_index] == len(lab_pre_group_student[key_list[category_index]]):
                    category_index += 1
                    if category_index == len(key_list):
                        category_index = 0

                current_student = lab_pre_group_student[key_list[category_index]][
                    key_index[category_index]]

                if not current_group or current_group.number < avg_size:
                    if group_list_index < len(group_list):
                        current_group = group_list[group_list_index]
                        group_list_index += 1
                    else:
                        new_group_num+=1
                        current_group = Group.objects.create(name=str(new_group_num), number=1,
                                                             project=project,
                                                             captain=current_student)
                        current_group.save()

                    project_student_group = Project_Student_Group.objects.create(group=current_group,
                                                                                 project=project,
                                                                                 student=current_student)

                    project_student_group.save()
                else:
                    project_student_group = Project_Student_Group.objects.create(group=current_group,
                                                                                 project=project,
                                                                                 student=current_student)
                    current_group.number += 1
                    current_group.save()
                    project_student_group.save()
                key_index[category_index] += 1
                count += 1
        response['msg'] = 'success'
        response['status'] = 200

        return JsonResponse(response)
