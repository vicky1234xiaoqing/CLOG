from django.db import models

# Create your models here.
class Course(models.Model):
    teacher = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    c_id = models.CharField(max_length=50)
    c_type = models.CharField(max_length=50)
    c_format = models.CharField(max_length=50)
    home = models.CharField(max_length=50)
    exper = models.CharField(max_length=50)
    exam = models.CharField(max_length=50)
    attend = models.CharField(max_length=50)
    c_intr = models.CharField(max_length=50)
    c_req = models.CharField(max_length=50)
    others = models.CharField(max_length=50)

    def __unicode__(self):
        return self.c_name
