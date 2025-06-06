from rest_framework import serializers
from datetime import datetime
import pytz

from .models import FitnessClass, ClassSlot
from user.serializers import CustomUserSerializer

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = CustomUserSerializer(read_only=True, fields=['id', 'name', 'email'])

    class Meta:
        model = FitnessClass
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ClassSlotSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True, fields=['id', 'name', 'instructor', 'class_type', 'date'])

    class Meta:
        model = ClassSlot
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('fields', None)
        self.target_timezone = kwargs.pop('target_timezone', None)
        super().__init__(*args, **kwargs)
        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        # Ensure the instance is correctly converted to a dict of serialized fields
        representation = super().to_representation(instance)

        if not self.target_timezone:
            self.target_timezone = self.context.get('target_timezone', None)

        if self.target_timezone:
            # Getting target timezone and Asia/Kolkata timezone
            target_tz = pytz.timezone(self.target_timezone)
            kolkata_tz = pytz.timezone('Asia/Kolkata')

            start_time = instance.start_time
            end_time = instance.end_time

            # Getting datetime object for Asia/Kolkata timezone
            start_time_kolkata = kolkata_tz.localize(datetime.combine(datetime.today(), start_time))
            end_time_kolkata = kolkata_tz.localize(datetime.combine(datetime.today(), end_time))

            # Convert to target timezone time object
            start_time_target = start_time_kolkata.astimezone(target_tz).time()
            end_time_target = end_time_kolkata.astimezone(target_tz).time()

            representation['start_time'] = start_time_target
            representation['end_time'] = end_time_target

            # Handle the date field in FitnessClassSerializer
            fitness_class_representation = representation['fitness_class']
            class_date_str = fitness_class_representation.get('date')
            class_date = datetime.strptime(class_date_str, "%Y-%m-%d").date()

            if class_date:
                # Convert the date to the target timezone if it's present
                class_date = datetime.combine(class_date, start_time)  
                class_date_kolkata = kolkata_tz.localize(class_date)
                class_date_target = class_date_kolkata.astimezone(target_tz).date()

                fitness_class_representation['date'] = class_date_target

        return representation