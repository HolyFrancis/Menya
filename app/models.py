from django.db import models
from django.utils.translation import gettext as _

from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    # class RoleType(models.TextChoices):
    #     ADMIN = "Admin", _("admin")
        
    
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    # role = models.CharField(max_length=100, null=True, blank=True, choice=)
    
class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Theme name"), null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
class Question(models.Model):
    class LevelType(models.TextChoices):
        EASY = "easy", _("easy level")
        AVERAGE = "average", _("average level")
        DIFFICULT = "difficult", _("difficult level")
    
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, null=False, blank=False)
    theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, related_name="questions", related_query_name="question")
    point = models.IntegerField(default=0)
    level = models.CharField(max_length=100, null=False, choices=LevelType.choices, default=LevelType.EASY)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.content
    

class QuestionResponse(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, null=False, blank=False)
    theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, related_name="theme_responses")
    question = models.ForeignKey("Question", on_delete=models.DO_NOTHING, related_name="responses", related_query_name="response")
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.content
    

class UserQuestionResponse(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, null=False, related_name="related_themes")
    question = models.ForeignKey("Question", on_delete=models.DO_NOTHING, related_name="related_questions" )
    question_response = models.ForeignKey("QuestionResponse", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def theme_score(self):
        score = 0
        theme_questions = self.theme.questions.all()
        
        for theme_question in theme_questions:
            theme_question_response = theme_question.responses.get(is_correct=True)
            if self.question_response == theme_question_response:
                score += theme_question.point
            else:
                score = 0
                    
        return score
    
# class UsersScore(models.Model):
#     theme = models.ForeignKey("Theme", on_delete=models.DO_NOTHING, null=False, related_name="theme_scores")
#     user = models.ForeignKey("MyUser", on_delete=models.DO_NOTHING, related_name="scores")
#     status = models.CharField(max_length=100, null=True, blank=True)
   
    
    
                    

            
    
        
        