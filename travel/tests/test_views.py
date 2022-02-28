from datetime import date, timedelta
from random import randint

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from travel.models import BudgetItem, Destination, Flight, Hotel, Trip
from user.models import User


class TestTripViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        cls.testuser = testuser
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )

    def test_trip_all(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:trip_all"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/trip_all.html")

    def test_trip_create_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:trip_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/trip_create.html")

    def test_trip_create_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:trip_create"),
            {
                "name": "Trip 1",
                "description": "Some trip description",
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=7),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:trip_mate_add", kwargs={"id": 8}))

    def test_trip_detail(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:trip_detail", kwargs={"id": self.trip.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/trip_detail.html")

    def test_trip_update_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:trip_update", kwargs={"id": self.trip.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/trip_create.html")

    def test_trip_update_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:trip_update", kwargs={"id": self.trip.id}),
            {
                "name": "Trip 1 updated",
                "description": "Some trip description",
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=7),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:trip_detail", kwargs={"id": self.trip.id}))

    def test_trip_mate_add_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:trip_mate_add", kwargs={"id": self.trip.id}), {"users": "test@test.com"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:trip_detail", kwargs={"id": self.trip.id}))


class TestBudgetAndItemViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        cls.testuser = testuser
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        cls.budgetitem = BudgetItem.objects.create(budget=cls.trip.budget, label="Label 1", quantity=1, item_price=120)

    def test_budget_detail(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:budget_detail", kwargs={"id": self.trip.budget.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/budget_detail.html")

    def test_budget_item_add_or_update_get(self):
        kwargs = {"id": self.trip.budget.id}
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:budget_item_add_or_update", kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:budget_detail", kwargs=kwargs))

    def test_budget_item_add_or_update_post_add(self):
        kwargs = {"id": self.trip.budget.id}
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:budget_item_add_or_update", kwargs=kwargs),
            {"budget": self.trip.budget.id, "label": "Sample budget item", "quantity": 1, "item_price": 100},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:budget_detail", kwargs=kwargs))

    def test_budget_item_add_or_update_post_update(self):
        kwargs = {"id": self.trip.budget.id}
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:budget_item_add_or_update", kwargs=kwargs),
            {
                "budget_id": self.budgetitem.id,
                "budget": self.trip.budget.id,
                "label": "Sample budget item",
                "quantity": 1,
                "item_price": 100,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:budget_detail", kwargs=kwargs))

    def test_budget_item_delete(self):
        kwargs = {"id": self.budgetitem.id}
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(reverse("travel:budget_item_delete", kwargs=kwargs))
        self.assertEqual(response.status_code, 204)

    def test_budget_item_delete_not_found(self):
        kwargs = {"id": 200}
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(reverse("travel:budget_item_delete", kwargs=kwargs))
        self.assertEqual(response.status_code, 400)


class TestDestinationViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        cls.testuser = testuser
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        cls.destination = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city1.png"
        )

    def test_destination_all(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:destination_all"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/destination_all.html")

    def test_destination_create_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:destination_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/destination_create.html")

    def test_destination_create_post(self):
        self.client.login(username="test@test.com", password="123")
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open("user/static/user/img/default.png", "rb").read(),
            content_type="image/jpeg",
        )
        response = self.client.post(
            reverse("travel:destination_create"),
            {
                "user": self.testuser,
                "name": "Destination new",
                "description": "destination description",
                "image": image,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:index"))

    def test_destination_update_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:destination_update", kwargs={"id": self.destination.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/destination_update.html")

    def test_destination_update_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:destination_update", kwargs={"id": self.destination.id}),
            {"name": "Destination new updated", "description": "Updated description"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:index"))

    def test_trip_destination_add_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:trip_destination_add", kwargs={"id": self.trip.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/trip_destination_add.html")

    def test_trip_destination_add_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:trip_destination_add", kwargs={"id": self.trip.id}), {"destinations": [self.destination.id]}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:trip_detail", kwargs={"id": self.trip.id}))


class TestHotelViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        cls.testuser = testuser
        cls.destination = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city1.png"
        )
        cls.hotel = Hotel.objects.create(
            name="Hotel 1", address="Hotel 1 address street 1", city=cls.destination, rate=4, checkin_date=date.today()
        )

    def test_destination_hotel_delete(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse(
                "travel:destination_hotel_delete", kwargs={"des_id": self.destination.id, "hotel_id": self.hotel.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:destination_update", kwargs={"id": self.destination.id}))

    def test_destination_hotel_add_or_update_add(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:destination_hotel_add_or_update", kwargs={"id": self.destination.id}),
            {
                "name": "Hotel 2",
                "address": "Street 2",
                "city": self.destination.id,
                "rate": 2,
                "checkin_date": date.today(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:destination_update", kwargs={"id": self.destination.id}))

    def test_destination_hotel_add_or_update_update(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:destination_hotel_add_or_update", kwargs={"id": self.destination.id}),
            {
                "hotel_id": self.hotel.id,
                "name": "Hotel 2",
                "address": "Street 2",
                "city": self.destination.id,
                "rate": 2,
                "checkin_date": date.today(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:destination_update", kwargs={"id": self.destination.id}))


class TestFlightViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        cls.testuser = testuser
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        cls.city_1 = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city1.png"
        )
        cls.city_2 = Destination.objects.create(
            user=cls.testuser, name="City 2", description="City 2 description", image="city2.png"
        )
        cls.flight = Flight.objects.create(
            user=cls.testuser, trip=cls.trip, from_loc=cls.city_1, to_loc=cls.city_2, checkin_date=timezone.now()
        )

    def test_flight_list(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("travel:flight_list", kwargs={"id": self.trip.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/flight_list.html")

    def test_flight_add_or_update_add(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:flight_add_or_update", kwargs={"id": self.trip.id}),
            {
                "user": self.testuser,
                "trip": self.trip,
                "from_loc": self.city_1.id,
                "to_loc": self.city_2.id,
                "checkin_date": timezone.now(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:flight_list", kwargs={"id": self.trip.id}))

    def test_flight_add_or_update_update(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("travel:flight_add_or_update", kwargs={"id": self.trip.id}),
            {
                "flight_id": self.flight.id,
                "user": self.testuser,
                "trip": self.trip,
                "from_loc": self.city_1.id,
                "to_loc": self.city_2.id,
                "checkin_date": timezone.now(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:flight_list", kwargs={"id": self.trip.id}))

    def test_flight_delete(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(reverse("travel:flight_delete", kwargs={"id": self.flight.id}))
        self.assertEqual(response.status_code, 204)

    def test_flight_delete_not_found(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(reverse("travel:flight_delete", kwargs={"id": randint(10, 100)}))
        self.assertEqual(response.status_code, 400)
