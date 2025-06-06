from rest_framework import serializers

from .models import ClassBooking
from fitness_class.serializers import ClassSlotSerializer
from user.serializers import CustomUserSerializer

    
class ClassBookingSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True, fields=['id', 'name', 'email'])

    class Meta:
        model = ClassBooking
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('fields', None)
        target_timezone = kwargs.pop('target_timezone', None)

        super().__init__(*args, **kwargs)

        # Pass target_timezone to ClassSlotSerializer if it's available
        if target_timezone:
            self.fields['class_slot'] = ClassSlotSerializer(read_only=True, target_timezone= target_timezone)
        else:
            self.fields['class_slot'] = ClassSlotSerializer(read_only=True)

        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)