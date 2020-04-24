from django.db import models

# Create your models here.
class Feedbcak(models.Model):
    problem = models.CharField(max_length=500)
    hepl = models.CharField(max_length=500)

    def __unicode__(self):
        return self.problem
