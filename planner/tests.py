from django.test import TestCase

# Create your tests here.

from django.test import TestCase

from .models import Meal

class MealModelTests(TestCase):

    def test_default_persons_is_4(self):
        m = Meal()
        self.assertEquals(m.persons, 4)
