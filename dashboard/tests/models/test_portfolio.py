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
		portfolio = Portfolio.objects.filter(user_profile=user.profile).first()

		self.assertEqual(str(portfolio), portfolio.name)
