import json

from django.test import TestCase, Client

from .models import User, Post, Follower, Comment

# Create your tests here.
# Models Test Case
class ModelsTest(TestCase):
    
    # Setup
    def setUp(self):
        # Create users
        harry = User.objects.create_user(username="Harry", email="harrypotter@example.com", password="12345")
        ron = User.objects.create_user(username="Hermione", email="hermionegranger@example.com", password="12345")
        hermione = User.objects.create_user(username="Ron", email="ronweasly@example.com", password="12345")
        
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
        post = Post.objects.get(pk=1)
        self.assertEqual(post.posted_by.username, "Harry")
        
        
    # Test number of likes
    def test_likes(self):
        p1 = Post.objects.get(pk=1)
        p2 = Post.objects.get(pk=2)
        self.assertEqual(p1.count_likes(), 2)
        self.assertEqual(p2.count_likes(), 0)
        
        
    # Test number of comments
    def test_post_comments(self):
        p = Post.objects.get(pk=2)
        self.assertEqual(p.comments.count(), 2)
        
        
    # Test followers
    def test_followers(self):
        harry = User.objects.get(username="Harry")
        self.assertEqual(harry.followers.count(), 3)
        
        
    # Test followings
    def test_followings(self):
        harry = User.objects.get(username="Harry")
        self.assertEqual(harry.followings.count(), 1)
        
        
    # Test valid follow
    def test_valid_follow(self):
        harry = User.objects.get(username="Harry")
        f = Follower.objects.get(followee=harry, follower=harry)   
        self.assertFalse(f.is_valid_follow())
    

# Views Test Case
class ViewsTest(TestCase):
    
    # Setup
    def setUp(self):
        harry = User.objects.create_user(username="Harry", email="harrypotter@example.com", password="12345")
        ron = User.objects.create_user(username="Ron", email="ronweasly@example.com", password="12345")
        hermione = User.objects.create_user(username="Hermione", email="hermionegranger@example.com", password="12345")

        for i in range(5):
            Post.objects.create(content="Hello, I'm Harry", posted_by=harry)
            Post.objects.create(content="Hello, Ron here!", posted_by=ron)
            Post.objects.create(content="Hi, I'm Hermione", posted_by=hermione)
            
        Follower.objects.create(followee=harry, follower=ron)
        Follower.objects.create(followee=harry, follower=hermione)
        
        Comment.objects.create(text="Hi!", owner=harry, post=Post.objects.get(pk=1))
        Comment.objects.create(text="Hello!", owner=hermione, post=Post.objects.get(pk=1))
        Comment.objects.create(text="Thanks!", owner=ron, post=Post.objects.get(pk=1))
        
        
    # Test create post feature
    def test_create_post(self):
        c = Client()
        
        # Test without login
        response = c.post("/create-post", data={"content": "Hello, World"})
        self.assertEqual(response.status_code, 302)
        
        # Test with login
        c.login(username="Harry", password="12345")
        response = c.post("/create-post", data={"content": "Hello, World"})
        self.assertEqual(response.status_code, 302)


    # Test all posts view
    def test_all_posts_view(self):
        c = Client()
        
        # Page 1
        response = c.get("/?page=1")
        self.assertEqual(len(response.context["posts"].object_list), 10)
        
        # Page 2
        response = c.get("/?page=2")
        self.assertEqual(len(response.context["posts"].object_list), 5)
    
    
    # Test followings posts
    def test_followings_posts_view(self):
        c = Client()
        
        # Test without login
        response = c.get("/followings")
        self.assertEqual(response.status_code, 302)
        
        # Test with login
        c.login(username="Ron", password="12345")
        response = c.get("/followings")
        
        self.assertEqual(len(response.context["posts"].object_list), 5)


    # Test profile page
    def test_profile_page(self):
        c = Client()
        user = User.objects.get(username="Harry")
        max_id = User.objects.order_by("-id").first()
        
        # Test invalid profile
        response = c.get(f"/profile/{max_id.id + 1}")
        self.assertEqual(response.status_code, 302)
        
        # Test profile without login
        response = c.get(f"/profile/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], user)
        self.assertFalse(response.context["is_following"])
        
        # Test profile with login and follow
        c.login(username="Ron", password="12345")
        response = c.get(f"/profile/{user.id}")
        self.assertTrue(response.context["is_following"])
        
        
    # Test like/unlike
    def test_like_unlike(self):
        c = Client()
        post = Post.objects.get(pk=1)
        max_id = Post.objects.order_by("-id").first()
        
        response = c.get(f"/like/{post.id}")
        self.assertEqual(response.status_code, 302)
        
        c.login(username="Ron", password="12345")
        
        response = c.get(f"/like/{max_id.id + 1}")
        self.assertEqual(response.status_code, 400)
        
        response = c.get(f"/like/{post.id}")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["liked"])
        
        response = c.get(f"/like/{post.id}")
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()["liked"])
        
    
    # Test follow/unfollow
    def test_follow_unfollow(self):
        c = Client()
        user = User.objects.get(username="Harry")
        max_id = User.objects.order_by("-id").first()
        
        c.login(username="Ron", password="12345")
        
        # Test invalid user follow
        response = c.get(f"/profile/{max_id.id + 1}/follow")
        self.assertEqual(response.status_code, 400)
        
        # Test self follow i.e. invalid follow
        ron = User.objects.get(username="Ron")
        response = c.get(f"/profile/{ron.id}/follow")
        self.assertEqual(response.json()["error"], "Invalid follow!")
        self.assertEqual(response.status_code, 400)
        
        # Test unfollow toggle as Ron already follows Harry
        response = c.get(f"/profile/{user.id}/follow")
        self.assertFalse(response.json()["follow"])
        
        # Test follow toggle
        response = c.get(f"/profile/{user.id}/follow")
        self.assertTrue(response.json()["follow"])
        

    # Test edit post
    def test_edit_post(self):
        c = Client()
        c.login(username="Harry", password="12345")
        rons_post = Post.objects.filter(posted_by=User.objects.get(username="Ron")).first()
        harrys_post = Post.objects.filter(posted_by=User.objects.get(username="Harry")).first()
        max_id = Post.objects.order_by("-id").first()
        
        # Test GET request
        response = c.get(f"/edit/{harrys_post.id}")
        self.assertEqual(response.status_code, 400)
        
        # Test POST request
        response = c.post(path=f"/edit/{harrys_post.id}", data={"content": "Edited post"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        
        # Test invalid post
        response = c.put(path=f"/edit/{max_id.id + 1}", data={"content": "Edited post"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        
        # Test forbidden edit request
        response = c.put(path=f"/edit/{rons_post.id}", data={"content": "Edited post"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        
        # Test valid request
        response = c.put(path=f"/edit/{harrys_post.id}", data={"content": "Edited post"}, content_type="application/json")
        self.assertEqual(response.status_code, 204)
        

    # Test delete post
    def test_delete_post(self):
        c = Client()
        c.login(username="Harry", password="12345")
        post = Post.objects.filter(posted_by=User.objects.get(username="Harry")).first()
        others_post = Post.objects.filter(posted_by=User.objects.get(username="Ron")).first()
        max_id = Post.objects.order_by("-id").first()

        # Test invalid post
        response = c.get(f"/delete/{max_id.id + 1}")
        self.assertEqual(response.status_code, 400)

        # Test forbidden user
        response = c.get(f"/delete/{others_post.id}")
        self.assertEqual(response.status_code, 403)

        # Test valid post deletion
        response = c.get(f"/delete/{post.id}")
        self.assertEqual(response.status_code, 200)
    
    
    # Test comment
    def test_comment(self):
        c = Client()
        c.login(username="Harry", password="12345")
        post = Post.objects.filter(posted_by=User.objects.get(username="Ron")).first()
        max_id = Post.objects.order_by("-id").first()
        
        # Test GET request
        response = c.get(f"/comment/{post.id}", data={"comment": "Hello, world"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        
        # Test invalid post
        response = c.post(f"/comment/{max_id.id + 1}", data={"comment": "Hello, world"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Post does not exist!")
        
        # Test valid post
        response = c.post(f"/comment/{post.id}", data={"comment": "Hello, world"}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        
    # Test delete comment
    def test_delete_comment(self):
        c = Client()
        c.login(username="Harry", password="12345")
        comment = Comment.objects.filter(owner=User.objects.get(username="Harry")).first()
        others_comment = Comment.objects.filter(owner=User.objects.get(username="Ron")).first()
        max_id = Comment.objects.order_by("-id").first()
        
        # Test invalid comment id
        response = c.get(f"/comment/delete/{max_id.id + 1}")
        self.assertEqual(response.status_code, 400)
        
        # Test forbidden request
        response = c.get(f"/comment/delete/{others_comment.id}")
        self.assertEqual(response.status_code, 403)
        
        # Test delete valid comment
        response = c.get(f"/comment/delete/{comment.id}")
        self.assertEqual(response.status_code, 200)
        
        
        
        