from django.test import TestCase
from users import models

class TestModels(TestCase):
    def test_my_user_manager_works(self):
        models.User.objects.create(
            username = "lilian-wanjiku",
            first_name= "lilian",
            last_name = "wanjiku",
            email = "lilianwanjiku@gmail.com")
        self.assertEqual(len(models.User.objects.all()), 1)
