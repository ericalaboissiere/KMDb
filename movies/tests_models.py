from django.test import TestCase
from .models import Movie
from datetime import date


class MovieTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lounch_date = date(year=1972, month=9, day=10)
        cls.movie = Movie.objects.create(
            title="Peixe grande",
            duration="75m",
            launch=cls.lounch_date,
            classification=14,
            synopsis="Lorem ipsum",
        )

    def test_iput_model_fields(self):
        self.assertIsInstance(self.movie.title, str)
        self.assertEqual(self.movie.title, "Peixe grande")

        self.assertIsInstance(self.movie.duration, str)
        self.assertEqual(self.movie.duration, "75m")

        self.assertIsInstance(self.movie.launch, date)
        self.assertEqual(self.movie.launch, "1972-09-10")

        self.assertIsInstance(self.movie.classification, int)
        self.assertEqual(self.movie.classification, 14)

        self.assertIsInstance(self.movie.synopsis, str)
        self.assertEqual(self.movie.synopsis, "Lorem ipsum")

    def test_defoult_model_field(self):
        self.assertEqual(self.movie.genre, None)
