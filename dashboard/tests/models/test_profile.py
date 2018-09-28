from django.test import TestCase
from django.shortcuts import get_object_or_404
from ..factories import UserFactory, StockFactory
from ...models import Profile, User


class ProfileTestCase(TestCase):
	def setUp(self):
		user = UserFactory.create(username='user_101')
		user2 = UserFactory.create(username='user_102')
		stock = StockFactory.create(user_profile=user.profile)

	def test_profile_string(self):
		user = get_object_or_404(User, username='user_101')

		self.assertEqual(str(user.profile), user.username)

	def test_has_stocks(self):
		user = get_object_or_404(User, username='user_101')
		user2 = get_object_or_404(User, username='user_102')

		self.assertEqual(user.profile.has_stocks(), True)
		self.assertEqual(user2.profile.has_stocks(), False)