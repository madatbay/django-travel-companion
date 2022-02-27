from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone
from travel.models import BudgetItem, Destination, Flight, Hotel, Trip
from user.models import User


class TestTripModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )

    def test_trip_str(self):
        self.assertEqual(self.trip.__str__(), "Trip 1")

    def test_trip_repr(self):
        self.assertEqual(self.trip.__repr__(), "<Trip: {}x{}>".format(self.trip.name, self.trip.id))

    def test_is_completed(self):
        self.assertFalse(self.trip.is_completed)


class TestBudgetAndItemModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        cls.budgetitem = BudgetItem.objects.create(budget=cls.trip.budget, label="BI 1", quantity=1, item_price=1)

    def test_trip_str(self):
        self.assertEqual(self.trip.budget.__str__(), "Trip 1 Budget")

    def test_get_total(self):
        self.assertEqual(self.trip.budget.get_total, 1.0)

    def test_budget_item_str(self):
        self.assertEqual(self.budgetitem.__str__(), "BI 1")

    def test_budget_item_get_subtotal(self):
        self.assertEqual(self.budgetitem.get_subtotal, 1.0)


class TestDestinationModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.destination = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city.png"
        )
        cls.destination2 = Destination.objects.create(
            user=cls.testuser,
            name="City 1",
            description="City 1 description",
        )

    def test_destination_str(self):
        self.assertEqual(self.destination.__str__(), "City 1")

    def test_destination_img_preview_no_img(self):
        self.assertEqual(self.destination2.img_preview, "Not set")

    def test_destination_img_preview(self):
        self.assertEqual(
            self.destination.img_preview, '<img src="{}" width="50" height="50" />'.format(self.destination.image.url)
        )


class TestHotelModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.destination = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city.png"
        )
        cls.hotel = Hotel.objects.create(
            name="Hotel 1",
            address="Hotel 1 address",
            city=cls.destination,
            rate=4,
            checkin_date=date.today() + timedelta(days=7),
        )

    def test_hotel_str(self):
        self.assertEqual(self.hotel.__str__(), "<Hotel - Hotel 1>")

    def test_hotel_repr(self):
        self.assertEqual(self.hotel.__repr__(), "<Hotel - Hotel 1>")


class TestFlightModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.trip = Trip.objects.create(
            user=cls.testuser,
            name="Trip 1",
            description="Some trip description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )
        cls.destination1 = Destination.objects.create(
            user=cls.testuser, name="City 1", description="City 1 description", image="city1.png"
        )
        cls.destination2 = Destination.objects.create(
            user=cls.testuser, name="City 2", description="City 2 description", image="city2.png"
        )
        cls.flight = Flight(
            user=cls.testuser,
            trip=cls.trip,
            from_loc=cls.destination1,
            to_loc=cls.destination2,
            checkin_date=timezone.now() + timedelta(days=7),
        )

    def test_is_active(self):
        self.assertTrue(self.flight.is_active)

    def test_flight_name(self):
        self.assertEqual(self.flight.flight_name, "Flight City 1-City 2")

    def test_flight_str(self):
        self.assertEqual(self.flight.__str__(), "Flight City 1-City 2")

    def test_flight_repr(self):
        self.assertEqual(self.flight.__repr__(), "<Flight City 1-City 2>")
