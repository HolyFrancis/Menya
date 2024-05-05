from django.test import TestCase

from app.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def test_serializer_valid_data(self):
        data = {"username": "jack", "email": "jack@gmail.com", "first_name": "jack", "last_name": "buntu"}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    