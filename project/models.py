from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from student.models import Student
from teacher.models import Teacher
from django.utils import timezone


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    teacher = models.ManyToManyField(Teacher, through="Teacher_Course")
    student = models.ManyToManyField(Student, through="Student_Course")
    terminate = models.BooleanField(default=False)

    class Meta:
        db_table = "Course"

    def __str__(self):
        return self.name


class Teacher_Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("teacher", "course"),)
        db_table = "Teacher_Course"

    def __str__(self):
        return str(self.teacher) + ' ' + str(self.course)


class Student_Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    character = models.CharField(max_length=10)
    lab = models.IntegerField()

    class Meta:
        unique_together = (("student", "course", "character"),)
        db_table = "Student_Course"


class Project(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    group_maxsize = models.IntegerField(null=True)
    group_minsize = models.IntegerField(default=0)
    index = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    across = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("name", "course"),)
        db_table = "Project"


class Project_Relation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    index = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "Project_Relation"


class Project_Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    document_path = models.CharField(max_length=100)

    class Meta:
        db_table = "Project_Document"


class Course_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sender = models.CharField(max_length=128, null=True)
    sender_character = models.CharField(max_length=10, null=True)
    send_time = models.CharField(max_length=128, null=True)
    content = models.TextField(null=True)

    class Meta:
        db_table = "Course_Message"


class Student_Message(models.Model):
    message = models.ForeignKey(Course_Message, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    needConfirm = models.BooleanField(null=True)
    secretMsg = models.CharField(max_length=128, null=True)
    accepted = models.BooleanField(null=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "Student_Message"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    project = models.ManyToManyField(Project, through="Project_Category")

    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.name


class Project_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField(null=True)

    class Meta:
        unique_together = (("category", "project"),)
        db_table = "Project_Category"


class Label(models.Model):
    name = models.CharField(max_length=100)

    student = models.ManyToManyField(Student, through="Student_Label")


    class Meta:
        db_table = "Label"

    def __str__(self):
        return self.name


class Student_Label(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    proficiency = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])


unique_together = (("student", "label"),)


class Meta:
    db_table = "Student_Label"


class Project_Label(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("student", "project", "label", "category"),)
        db_table = "Project_Label"


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    number = models.IntegerField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    grade = models.FloatField(null=True)
    captain = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = "Group"

    def __str__(self):
        return self.name


class Group_Desire_Label(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("group", "label"),)
        db_table = "Group_Desire_Label"


class Project_MarkSheet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    proportion = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(0)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "Project_MarkSheet"


class Group_Grades(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    markSheet = models.ForeignKey(Project_MarkSheet, on_delete=models.CASCADE)
    grade = models.FloatField(default=0,
                              validators=[MaxValueValidator(100), MinValueValidator(0)])
    comment = models.TextField(null=True)

    class Meta:
        db_table = "Group_Grades"


class Project_Student_Group(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField(default=0,
                              validators=[MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        unique_together = (("project", "student"),)
        db_table = "Project_Student_Group"


class Group_File(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=500)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "Group_File"


class File_Log(models.Model):
    file = models.ForeignKey(Group_File, on_delete=models.CASCADE)
    operation = models.CharField(max_length=10, default='Upload')
    op_stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    op_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "File_Log"


class Project_Presentation(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    duration = models.IntegerField()
    index = models.IntegerField()

    class Meta:
        db_table = "Project_Presentation"

    def __str__(self):
        return self.name


class Presentation_Schedule(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    project_presentation = models.ForeignKey(Project_Presentation, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("start", "end", "group"))
        db_table = "Presentation_Schedule"

    def __str__(self):
        return self.project_presentation.name + self.start.strftime(' %Y-%m-%d : %H:%M') + "——" + self.end.strftime(
            '%H:%M')
