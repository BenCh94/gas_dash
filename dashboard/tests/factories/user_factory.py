import factory
from ...models import User


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	username = factory.Sequence(lambda n: 'testuser{0}'.format(n))
	email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
