from django.db import models

from fitness_class.models import ClassSlot
from user.models import CustomUser

# Create your models here.
class ClassBooking(models.Model):
    class_slot = models.ForeignKey(ClassSlot, on_delete=models.CASCADE, related_name='class_slot')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.user.name