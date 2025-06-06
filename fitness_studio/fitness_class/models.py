from django.db import models

from user.models import CustomUser

# Create your models here.
class FitnessClass(models.Model):

    class FitnessClassType(models.TextChoices):
        YOGA = 'yoga'
        ZUMBA = 'zumba'
        HIIT = 'hiit'

    name = models.CharField(max_length=100, unique=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructor')
    class_type = models.CharField(max_length=10, choices=FitnessClassType.choices)
    date = models.DateField()
    member_max_count = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.name
    
class ClassSlot(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='fitness_class')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.fitness_class.name