from django.test import TestCase

from .models import User, Post, Follower, Comment

# Create your tests here.
class ModelsTest(TestCase):
    
    # Setup
    def setUp(self):
        # Create users
        harry = User.objects.create(username="Harry", email="harrypotter@example.com", password="12345")
        ron = User.objects.create(username="Hermione", email="hermionegranger@example.com", password="12345")
        hermione = User.objects.create(username="Ron", email="ronweasly@example.com", password="12345")
        
        # Create posts
        p1 = Post.objects.create(content="Hello, world! My name is Harry", posted_by=harry)
        p2 = Post.objects.create(content="Hello! Ron here!", posted_by=ron)
        p3 = Post.objects.create(content="Hi! I'm Hermione", posted_by=hermione)
        
        # Create likes
        p1.likes.add(ron)
        p1.likes.add(hermione)
        p3.likes.add(harry)
        
        # Create comments
        Comment.objects.create(text="Hi! Ron", owner=harry, post=p2)
        Comment.objects.create(text="Hello! Harry", owner=ron, post=p1)
        Comment.objects.create(text="Hello, Ron!", owner=hermione, post=p2)
        
        # Create follow
        Follower.objects.create(followee=harry, follower=ron)
        Follower.objects.create(followee=harry, follower=hermione)
        Follower.objects.create(followee=harry, follower=harry)
        
    # Test number of posts
    def test_posts(self):
        self.assertEqual(Post.objects.count(), 3)
        
    # Test post
    def test_post(self):
        self.assertEqual(Post.objects.get(pk=1).posted_by.username, "Harry")
        
    # Test number of likes
    def test_likes(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.get_likes(), 2)
        
    # Test number of comments
    def test_post_comments(self):
        p = Post.objects.get(pk=2)
        self.assertEqual(p.comments.count(), 2)
        
    # Test valid follow
    def test_follow(self):
        harry = User.objects.get(username="Harry")
        f = Follower.objects.get(followee=harry, follower=harry)
                
        self.assertFalse(f.is_valid_follow())
        self.assertEqual(Follower.objects.filter(followee=harry).count(), 3)
        
    
