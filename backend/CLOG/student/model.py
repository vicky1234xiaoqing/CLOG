from django.db import models

# Create your models here.
class Student(models.Model):
    student = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    c_id = models.CharField(max_length=50)
    c_type = models.CharField(max_length=50)
    c_intr = models.CharField(max_length=50)
    c_req = models.CharField(max_length=50)
    others = models.CharField(max_length=50)
    e_grade = models.CharField(max_length=50)

    def __unicode__(self):
        return self.student
