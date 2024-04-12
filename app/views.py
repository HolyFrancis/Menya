from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins as drf_mixins
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from app.serializers import *

# Create your views here.

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UserLoginAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        user = request.user
        
        token = self.serializer_class.get_token(user)
        print(f"\n\n\n\n{user}\n\n\n")
        response.data = {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": str(token.access_token),
            "refresh": str(token),
        }
        
        return response


    
class ThemeListAPIView(ListAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
    authentication_classes = [BasicAuthentication]
    
    
class ThemeCreateAPIView(APIView):
    serializer_class = ThemeSerializer
    authentication_classes = [BasicAuthentication]
    
    def post(self, request):
        serializer = self.serializer_class(data=self.request.data, context={"request": self.request})
        
        
        serializer.is_valid(raise_exception=True)
        theme = serializer.validated_data["name"]
        description = serializer.validated_data["description"]
        
        new_theme = Theme.objects.create(name=theme, description=description)
        
        if new_theme:
            return Response (
                {
                    "success": True,
                    "response_message": "the new theme created succesfully",
                    "response_data": {
                        'theme': new_theme.name
                    }
                }
            ) 
        else: 
            return Response (
                {
                    "success": False,
                    "response_message": "failed to create the theme",
                    
                }
            )    


class QuestionViewset(GenericViewSet,
                      drf_mixins.CreateModelMixin, 
                      drf_mixins.ListModelMixin,
                      drf_mixins.UpdateModelMixin,
                      drf_mixins.DestroyModelMixin
        ):
    
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [TokenAuthentication]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return self.serializer_class
        return QuestionListSerializer
    

class QuestionResponsesViewset(
    GenericViewSet, 
    drf_mixins.CreateModelMixin,
    drf_mixins.ListModelMixin,
    drf_mixins.UpdateModelMixin,
):
    permission_classes = [AllowAny]
    serializer_class = QuestionResponsesSerializer
    queryset = QuestionResponse.objects.all()
    authentication_classes  = [TokenAuthentication]
    
    def get_queryset(self):
        question = self.request.query_params.get("question")
        if question:
            queryset = self.queryset.filter(question=question)
            return queryset
        return self.queryset

class UserQuestionResponseViewset(GenericViewSet,drf_mixins.CreateModelMixin,
    drf_mixins.ListModelMixin,
    drf_mixins.UpdateModelMixin,
):
    permission_classes = [AllowAny]
    queryset = UserQuestionResponse.objects.all()
    serializer_class = UserQuestionResponseSerializer
    


# class UserQuestionResponseCreateAPIView(CreateAPIView):
#     serializer_class = UserQuestionResponseCreateSerializer
    
#     permission_classes = [AllowAny]
    
   
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
        
#     def create(self, request, *args, **kwargs):
#         # Check if the user has already submitted a response for this question
#         user_profile = self.request.user
#         print(f"\n\n\n\n\n{user_profile}\n\n\n\n")
#         if not self.request.user.is_authenticated:
#             return Response ({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
#         question_id = self.request.data.get('question_response')
#         theme = self.request.data.get('theme')
        
#         if question_id is None or theme is None:
#             return Response ({"detail": 'you have to include theme and question_response'})
        
#         if UserQuestionResponse.objects.filter(user=user_profile, question_response=question_id, theme=theme).exists():
#             return Response({'detail': 'You have already submitted a response for this question.'}, status=status.HTTP_400_BAD_REQUEST)

#         return super().create(request, *args, **kwargs)

    
class UserQuestionResponseListAPIView(ListAPIView):
    serializer_class = UserQuestionResponseSerializer
    queryset = UserQuestionResponse.objects.all()