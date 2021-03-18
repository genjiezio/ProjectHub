from django.contrib import messages, admin
from django.shortcuts import redirect, render
from django.urls import path, re_path
from django.utils.translation import gettext as _, gettext_lazy
from padmin.forms import ExportCsvMixin, TeacherImportForm

from teacher.models import Teacher


# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin, ExportCsvMixin):
    # change_list_template = "admin/padmin/teacher_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_accounts/', self.import_accounts),
        ]
        return my_urls + urls

    def import_accounts(self, request):
        form = TeacherImportForm()
        payload = {"head": "Teacher Accounts", "form": form}
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
                    teacher_data = line.split(",")
                    if teacher_data:
                        try:
                            account = teacher_data[0].strip()
                            password = teacher_data[1].strip()
                            email = teacher_data[2].strip()
                            teacher = Teacher.objects.create(account=account, password=password,
                                                             email=email)
                            teacher.save()
                            success += 1
                        except Exception as e:
                            msg.append({'id': i + 2, 'key': 'Account: ' + account, 'error': str(e)})
                if msg:
                    payload['msg'] = msg
                    self.message_user(request,
                                      (
                                          "%(success)d account(s) import success. %(error)d account(s) import error.") % {
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
