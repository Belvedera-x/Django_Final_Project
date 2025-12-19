import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import random
from datetime import timedelta

import factory
from factory import fuzzy
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from homefinder_app.utils import update_housing_rating
from homefinder_app.models import(
    Housing,
    User,
    Review,
    Booking
)
from homefinder_app.enums import Role, Gender, HousingType, BookingStatus

faker_ = Faker()



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda obj: faker_.unique.user_name())
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    role = factory.LazyAttribute(
        lambda obj: random.choice(list(Role)).value
    )

    gender = factory.LazyAttribute(
        lambda obj: random.choice(list(Gender)).value
    )

    birth_date = factory.Faker(
        'date_of_birth', minimum_age=18, maximum_age=78
    )
    # age = factory.LazyAttribute(lambda obj: timezone.now().year - obj.birth_date.year)
    phone = factory.LazyAttribute(lambda obj: f"+{faker_.msisdn()[:12]}")

    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    password = factory.LazyFunction(lambda: make_password("sergii"))



class HousingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Housing

    title = factory.LazyAttribute(
        lambda o: f"{o.number_of_rooms}-room {o.housing_type} in {o.city}"
    )
    description = factory.Faker('text', max_nb_chars=255)

    owner = factory.SubFactory(
        UserFactory,
        role=Role.owner.value
    )

    city = factory.Faker('city')
    district = factory.LazyAttribute(
        lambda _: f"{faker_.city()}-{faker_.city_suffix()}"
    )
    street = factory.Faker('street_address')

    price = fuzzy.FuzzyDecimal(50, 5000, precision=2)
    number_of_rooms = fuzzy.FuzzyInteger(1, 5)
    housing_type = factory.LazyAttribute(
        lambda obj: random.choice(list(HousingType)).value
    )
    available = factory.Faker('boolean')


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    housing = factory.SubFactory(HousingFactory)
    guest = factory.SubFactory(
        UserFactory,
        role=Role.tenant.value
    )

    start_date = factory.LazyFunction(
        lambda: timezone.now()
    )

    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timedelta(days=random.randint(1, 30))
    )

    status = factory.LazyAttribute(
        lambda obj: random.choice(list(BookingStatus)).name
    )

    total_price = factory.LazyAttribute(
        lambda obj: (obj.end_date - obj.start_date).days * obj.housing.price
    )

    created_at = factory.LazyFunction(timezone.now)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    housing = factory.SubFactory(HousingFactory)
    author = factory.SubFactory(
        UserFactory,
        role=Role.tenant.value
    )

    text = factory.Faker('text', max_nb_chars=600)
    created_at = factory.LazyFunction(timezone.now)
    rating = fuzzy.FuzzyInteger(1, 5)

    @factory.post_generation
    def update_rating(self, create, extracted, **kwargs):
        if not create:
            return
        update_housing_rating(self.housing)



if __name__ == "__main__":
    print("!!!!!!   HERE WE GO   !!!!!!")

    users = UserFactory.create_batch(2)

    housings = []
    for user in users:
        if user.role == Role.owner:
            housings.extend(
                HousingFactory.create_batch(
                    random.randint(1, 3),
                    owner=user
                )
            )

    for housing in housings:
        ReviewFactory.create_batch(
            random.randint(1, 5),
            housing=housing
        )

    bookings = []

    for housing in housings:
        bookings.extend(
            BookingFactory.create_batch(
                random.randint(0, 3),
                housing=housing,
                guest=UserFactory(role=Role.tenant)
            )
        )

    print("!!!!!!   DONE   !!!!!!")