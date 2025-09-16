from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    nickname = serializers.CharField(max_length=30)

    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        email = (data.get('email') or '').strip()
        phone = (data.get('phone') or '').strip()
        if not email and not phone:
            raise serializers.ValidationError("Either email or phone number must be provided.")
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            nickname=validated_data.get('nickname'),
            email=(validated_data.get('email') or None),
            phone=(validated_data.get('phone') or None),
            birth_date=validated_data.get('birth_date'),
        )
        
        
class LoginSerializer(serializers.TokenObtainPairSerializer):
    def valiedate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = User.objects.filter(
            Q(username=username)
        ).first()
        
        if not user or not user.check_password(password):
            raise self.error_messages['no_active_account']
        
        attrs = {
            'username': user.username,
            'password': password,
        }
        data = super().validate(attrs)
        
        return data
