from rest_framework import serializers

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
    
    
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = '__all__'
        
class UserQuestionResponseSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserQuestionResponse
        fields = ['user', 'theme', 'question_response', 'user_score']
        
    def get_user_score(self, obj):
        if obj.theme_score:
            user_score = obj.theme_score
            
            return user_score