from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DoctorDetail(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='doctor_detail')
    qualification = models.CharField(max_length=16)

    def __str__(self):
        return self.auth_user.first_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # TODO: override and save the User first and save the details of doctor with
        #  the saved auth_user as a foreign key
        super().save()
