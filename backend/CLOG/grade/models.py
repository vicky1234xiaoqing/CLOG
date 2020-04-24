from django.db import models

class Grade(models.Model):
    grade = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    item = models.CharField(max_length=500)
    c_id = models.CharField(max_length=500)

    def __unicode__(self):
        return self.username
