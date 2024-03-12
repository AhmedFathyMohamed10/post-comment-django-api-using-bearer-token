from django.test import TestCase
from django.contrib.auth.models import User
from .models import Posts, Comment
from .serializers import PostSerializer


class PostsModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Posts.objects.create(user_id=self.user, title='Test Title', content='Test Content')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Title')

    def test_post_user_relationship(self):
        # Ensure that the post is associated with the correct user
        self.assertEqual(self.post.user_id, self.user)

    def test_post_title_max_length(self):
        # Ensure that the title field has the correct max length
        max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_post_content_not_blank(self):
        # Ensure that the content field is not blank
        self.assertIsNotNone(self.post.content)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testusercomment')
        self.post = Posts.objects.create(user_id=self.user, title='Test Title', content='Test Content')
        self.comment = Comment.objects.create(post=self.post, user=self.user, comment='Test Comment')

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'Test Comment')

    def test_comment_post_relationship(self):
        self.assertEqual(self.comment.post, self.post)


# Here i test my serializers.py also to check serialization and deserialization
class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post_data = {'title': 'Test Title', 'content': 'Test Content'}
        self.post = Posts.objects.create(user_id=self.user, **self.post_data)

    def test_post_serializer_serialization(self):
        serializer = PostSerializer(instance=self.post)
        expected_data = {'title': 'Test Title', 'content': 'Test Content'}
        self.assertEqual(serializer.data, expected_data)

    def test_post_serializer_deserialization(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())
        post_instance = serializer.save(user_id=self.user)
        self.assertIsInstance(post_instance, Posts)