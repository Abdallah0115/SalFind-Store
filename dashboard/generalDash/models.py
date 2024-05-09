from django.db import models
from django.contrib.auth.models import AbstractUser ,Group, Permission ,User

class guest(AbstractUser):
    full_name = models.CharField(max_length=255,default="")
    email = models.EmailField(null=False)
    groups = models.ManyToManyField(Group, related_name='guest_users')
    user = models.OneToOneField(User, related_name='guest_user', on_delete=models.CASCADE, primary_key=True)
    user_permissions = models.ManyToManyField(Permission, related_name='guest_users')

class sess(models.Model):

    name = models.CharField(max_length=100)

    description = models.CharField(max_length=1000)

    gues = models.ForeignKey(guest, on_delete=models.CASCADE , default="Others")

    csv_file = models.FileField(upload_to='csv_files/')

    last_used = models.DateTimeField(auto_now_add=True)


class guestGroup(models.Model):
    guest = models.ForeignKey(guest, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'generalDash_guest_groups'
        managed = False