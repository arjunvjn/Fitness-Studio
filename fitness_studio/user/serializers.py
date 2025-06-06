from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = {}
        token = super().get_token(user)
        
        # Custom field data that will be added to the jwt payload
        token['name'] = user.name
        token['role'] = user.role
        
        return token
    
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
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