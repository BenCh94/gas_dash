from django.test import TestCase
from django.shortcuts import get_object_or_404
from ..factories import UserFactory, PortfolioFactory
from ...models import Portfolio, User


class PortfolioTestCase(TestCase):
	def setUp(self):
		user = UserFactory.create(username='testuser')
		portfolio = PortfolioFactory(user_profile=user.profile, name=user.username)

	def test_portfolio_string(self):
		user = get_object_or_404(User, username='testuser')
		portfolio = get_object_or_404(Portfolio, user_profile=user.profile)

		self.assertEqual(str(portfolio), portfolio.name)
