from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name',]
        
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2' ]
        
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("passwords didnt match")
        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create(username=validated_data["username"], email=validated_data["email"], 
                                     first_name=validated_data["first_name"], last_name=validated_data["last_name"])
        
        user.set_password(validated_data["password"])
        user.save()
        
        return user
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=100, read_only=True)
    password = serializers.CharField(max_length=100, read_only=True)
    
    # def validate(self, attrs, data):
    #     username = data.get("username")
    #     password = data.get("password")
        
    #     data = super().validate(attrs)
    #     if username is None:
    #         return serializers.ValidationError("username is required to log in")
    #     elif password is None:
    #         return serializers.ValidationError("the password is required")
    #     else:
    #         user = authenticate(username=username, password=password)
            
    #     return self.get_token(user)
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add custom data to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # Add any other user-related data you want to include
        }

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # token['email'] = user.email
        token['user_id'] = user.id
        # ...

        return token
    
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ["id", "name", "description"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "content", "theme", "point", "level"]


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["content", "theme"]

class QuestionResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ["id", "content", "theme","question", "is_correct"]
        
class UserQuestionResponseSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserQuestionResponse
        fields = ['id', 'theme', 'question', 'question_response', 'user_score']
        
    def get_user_score(self, obj):
        if obj.theme_score:
            user_score = obj.theme_score
            
            return user_score
        
class UserQuestionResponseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserQuestionResponse
        fields = ['id', 'theme', 'question_response',]