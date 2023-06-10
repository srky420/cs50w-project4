from django.test import TestCase

from .models import User, Post, Follower, Comment

# Create your tests here.
class ModelsTest(TestCase):
    
    # Setup
    def setUp(self):
        # Create users
        u1 = User.objects.create(username="Harry", email="harrypotter@example.com", password="12345")
        u2 = User.objects.create(username="Hermione", email="hermionegranger@example.com", password="12345")
        u3 = User.objects.create(username="Ron", email="ronweasly@example.com", password="12345")
