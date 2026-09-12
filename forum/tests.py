from django.contrib.auth.models import User
from django.test import TestCase

from .models import Post, Thread
class ForumTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='student', password='test-pass-123')
		self.moderator = User.objects.create_user(
			username='moderator', password='test-pass-123', is_staff=True
		)
		self.thread = Thread.objects.create(
			title='Важливе оголошення', content='Текст оголошення', user=self.moderator
		)

	def test_home_and_thread_detail_render(self):
		self.assertContains(self.client.get('/'), self.thread.title)
		response = self.client.get(f'/threads/{self.thread.id}/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.thread.content)

	def test_authenticated_user_can_reply(self):
		self.client.login(username='student', password='test-pass-123')
		response = self.client.post(
			f'/threads/{self.thread.id}/', {'content': 'Моя відповідь'}
		)
		self.assertRedirects(response, f'/threads/{self.thread.id}/')
		self.assertTrue(Post.objects.filter(content='Моя відповідь').exists())

	def test_user_can_toggle_like(self):
		post = Post.objects.create(thread=self.thread, user=self.user, content='Відповідь')
		self.client.login(username='student', password='test-pass-123')
		url = f'/posts/{post.id}/reaction/like/'
		self.client.post(url)
		self.assertTrue(post.likes.filter(pk=self.user.pk).exists())
		self.client.post(url)
		self.assertFalse(post.likes.filter(pk=self.user.pk).exists())

	def test_only_staff_can_create_threads(self):
		self.client.login(username='student', password='test-pass-123')
		self.assertEqual(self.client.get('/threads/create/').status_code, 403)
		self.client.login(username='moderator', password='test-pass-123')
		response = self.client.post(
			'/threads/create/', {'title': 'Нова тема', 'content': 'Новий текст'}
		)
		self.assertRedirects(response, '/threads/')

