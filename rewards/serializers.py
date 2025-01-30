from rest_framework import serializers
from .models import CustomUser, App, Task, UserProfile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_admin')

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'
        read_only_fields = ('created_by',)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'status', 'submitted_at')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    recent_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'points_earned', 'tasks_completed', 'recent_activities']

    def get_recent_activities(self, obj):
        tasks = Task.objects.filter(user=obj.user).order_by('-submitted_at')[:5]
        return [{
            'app_name': task.app.name,
            'status': task.status,
            'timestamp': task.submitted_at
        } for task in tasks]
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")