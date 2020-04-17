from django.db import models

# Create your models here.
class User(models.Model):
    Email = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    StudentID = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    Grade = models.CharField(max_length=50)
    newer = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username
