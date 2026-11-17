from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import News, Comment

User = get_user_model()

class NewsFlashMessagesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='author@example.com',
            full_name='Author Name',
            phone='123456789',
            password='password123'
        )
        self.client = Client()
        self.client.login(email='author@example.com', password='password123')

    def test_news_create_message(self):
        response = self.client.post(
            reverse('news_create'),
            {
                'title': 'New Story Headline',
                'content': 'Story content text for test.'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('published successfully' in str(m) for m in messages_list))

    def test_news_update_message(self):
        news = News.objects.create(author=self.user, title='Original Title', content='Original content')
        response = self.client.post(
            reverse('news_update', args=[news.id]),
            {
                'title': 'Updated Title',
                'content': 'Updated content'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated successfully' in str(m) for m in messages_list))

    def test_news_delete_message(self):
        news = News.objects.create(author=self.user, title='Title to delete', content='Content')
        response = self.client.post(reverse('news_delete', args=[news.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('deleted successfully' in str(m) for m in messages_list))


class CommentAsyncTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testauthor@example.com',
            full_name='Test Author',
            phone='123456789',
            password='password123'
        )
        self.reader = User.objects.create_user(
            email='testreader@example.com',
            full_name='Test Reader',
            phone='987654321',
            password='password123'
        )
        self.news = News.objects.create(
            author=self.user,
            title='Test News Headline',
            content='Test News Content for editorial blog.'
        )
        self.client = Client()

    def test_comment_create_async(self):
        self.client.login(email='testreader@example.com', password='password123')
        response = self.client.post(
            reverse('news_detail', args=[self.news.id]),
            {'content': 'This is an insightful comment!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['comment']['content'], 'This is an insightful comment!')
        self.assertEqual(data['comments_count'], 1)

    def test_comment_update_async(self):
        comment = Comment.objects.create(news=self.news, author=self.reader, content='Initial text')
        self.client.login(email='testreader@example.com', password='password123')
        response = self.client.post(
            reverse('comment_update', args=[comment.id]),
            {'content': 'Updated content text'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['comment']['content'], 'Updated content text')
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated content text')

    def test_comment_delete_async(self):
        comment = Comment.objects.create(news=self.news, author=self.reader, content='Text to delete')
        self.client.login(email='testreader@example.com', password='password123')
        response = self.client.post(
            reverse('comment_delete', args=[comment.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['comments_count'], 0)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
