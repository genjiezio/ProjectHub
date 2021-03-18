from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path, re_path
from django.utils.translation import gettext as _, gettext_lazy
from padmin.forms import ExportCsvMixin, CourseImportForm, StuCourseImportForm, TeaCourseImportForm

from project.models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Project_Document)
admin.site.register(Course_Message)
admin.site.register(Student_Message)
admin.site.register(Category)
admin.site.register(Project_Category)
admin.site.register(Label)
admin.site.register(Student_Label)
admin.site.register(Project_Label)
admin.site.register(Project_Relation)
admin.site.register(Group)
admin.site.register(Project_MarkSheet)
admin.site.register(Group_Grades)
admin.site.register(Project_Student_Group)
admin.site.register(Group_File)
admin.site.register(Project_Presentation)
admin.site.register(Presentation_Schedule)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin, ExportCsvMixin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_courses/', self.import_courses),
        ]
        return my_urls + urls

    def import_courses(self, request):
        form = CourseImportForm()
        payload = {"head": "Courses", "form": form}
        if request.method == "POST":
            file = request.FILES.get("csv_file")
            if not file:
                self.message_user(request, ("Please select a file."), messages.WARNING)
                return render(request, "admin/padmin/csv_form.html", payload)
            elif file.name.endswith('.csv'):
                msg = []
                success = 0
                file_data = file.read().decode("utf-8")
                lines = file_data.split("\r\n")
                for i, line in enumerate(lines[1:]):
                    course_data = line.split(",")
                    if len(course_data) >= 2:
                        try:
                            name = course_data[0].strip()
                            description = course_data[1].strip()
                            course = Course.objects.create(name=name, description=description)
                            course.save()
                            success += 1
                        except Exception as e:
                            msg.append({'id': i + 2, 'key': 'Course Name: ' + name, 'error': str(e)})
                    else:
                        msg.append(
                            {'id': i + 2, 'key': 'line data: ' + str(line), 'error': "Number of fields inconsistent."})
                if msg:
                    payload['msg'] = msg
                    self.message_user(request,
                                      (
                                          "%(success)d course(s) import success. %(error)d course(s) import error.") % {
                                          "success": success, "error": len(msg)}, messages.WARNING)
                    return render(request, "admin/padmin/csv_form.html", payload)
                else:
                    self.message_user(request, _("\'%(file)s\' imports success without error.") % {"file": file.name},
                                      messages.SUCCESS)
                    return redirect("..")

            else:
                self.message_user(request, _("\'%(file)s\' is not a csv file.") % {"file": file.name}, messages.ERROR)
                return render(request, "admin/padmin/csv_form.html", payload)

        return render(request, "admin/padmin/csv_form.html", payload)


@admin.register(Student_Course)
class StuCourseAdmin(admin.ModelAdmin, ExportCsvMixin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_student_courses/', self.import_student_courses),
        ]
        return my_urls + urls

    def import_student_courses(self, request):
        form = StuCourseImportForm()
        payload = {"head": "Student List in Courses", "form": form}
        if request.method == "POST":
            file = request.FILES.get("csv_file")
            if not file:
                self.message_user(request, ("Please select a file."), messages.WARNING)
                return render(request, "admin/padmin/csv_form.html", payload)
            elif file.name.endswith('.csv'):
                msg = []
                success = 0
                file_data = file.read().decode("utf-8")
                lines = file_data.split("\r\n")
                for i, line in enumerate(lines[1:]):
                    cour_stu_data = line.split(",")
                    if len(cour_stu_data) >= 4:
                        try:
                            course_name = cour_stu_data[0].strip()
                            student_account = cour_stu_data[1].strip()
                            character = cour_stu_data[2].strip()
                            lab = int(cour_stu_data[3].strip())
                            course = Course.objects.get(name=course_name)
                            student = Student.objects.get(account=student_account)
                            cour_stu = Student_Course.objects.create(course=course, student=student,
                                                                     character=character, lab=lab)
                            cour_stu.save()

                            success += 1
                        except Exception as e:
                            msg.append(
                                {'id': i + 2, 'key': "Course: " + cour_stu_data[0] + ", Student: " + cour_stu_data[1],
                                 'error': str(e)})
                    else:
                        msg.append(
                            {'id': i + 2, 'key': 'line data: ' + str(line), 'error': "Number of fields inconsistent."})

                if msg:
                    payload['msg'] = msg
                    self.message_user(request,
                                      (
                                          "%(success)d line(s) import success. %(error)d line(s) import error.") % {
                                          "success": success, "error": len(msg)}, messages.WARNING)
                    return render(request, "admin/padmin/csv_form.html", payload)
                else:
                    self.message_user(request, _("\'%(file)s\' imports success without error.") % {"file": file.name},
                                      messages.SUCCESS)
                    return redirect("..")

            else:
                self.message_user(request, _("\'%(file)s\' is not a csv file.") % {"file": file.name}, messages.ERROR)
                return render(request, "admin/padmin/csv_form.html", payload)

        return render(request, "admin/padmin/csv_form.html", payload)


@admin.register(Teacher_Course)
class TeaCourseAdmin(admin.ModelAdmin, ExportCsvMixin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_teacher_courses/', self.import_teacher_courses),
        ]
        return my_urls + urls

    def import_teacher_courses(self, request):
        form = TeaCourseImportForm()
        payload = {"head": "Teacher List in Courses", "form": form}
        if request.method == "POST":
            file = request.FILES.get("csv_file")
            if not file:
                self.message_user(request, ("Please select a file."), messages.WARNING)
                return render(request, "admin/padmin/csv_form.html", payload)
            elif file.name.endswith('.csv'):
                msg = []
                success = 0
                file_data = file.read().decode("utf-8")
                lines = file_data.split("\r\n")
                for i, line in enumerate(lines[1:]):
                    cour_tea_data = line.split(",")
                    if len(cour_tea_data) >= 2:
                        try:
                            course_name = cour_tea_data[0].strip()
                            teacher_account = cour_tea_data[1].strip()
                            course = Course.objects.get(name=course_name)
                            teacher = Teacher.objects.get(account=teacher_account)
                            cour_tea = Teacher_Course.objects.create(course=course, teacher=teacher)
                            cour_tea.save()
                            success += 1
                        except Exception as e:
                            msg.append(
                                {'id': i + 2, 'key': "Course: " + cour_tea_data[0] + ", Teacher: " + cour_tea_data[1],
                                 'error': str(e)})
                    else:
                        msg.append(
                            {'id': i + 2, 'key': 'line data: ' + str(line), 'error': "Number of fields inconsistent."})

                if msg:
                    payload['msg'] = msg
                    self.message_user(request,
                                      (
                                          "%(success)d line(s) import success. %(error)d line(s) import error.") % {
                                          "success": success, "error": len(msg)}, messages.WARNING)
                    return render(request, "admin/padmin/csv_form.html", payload)
                else:
                    self.message_user(request, _("\'%(file)s\' imports success without error.") % {"file": file.name},
                                      messages.SUCCESS)
                    return redirect("..")

            else:
                self.message_user(request, _("\'%(file)s\' is not a csv file.") % {"file": file.name}, messages.ERROR)
                return render(request, "admin/padmin/csv_form.html", payload)

        return render(request, "admin/padmin/csv_form.html", payload)