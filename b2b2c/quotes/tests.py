from django.test import TestCase
from django.urls import reverse

from .models import Branch, Product, Quote
from .views import calculate_quote_price


class QuotePriceTest(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name="Travel")
        self.product = Product.objects.create(branch=self.branch, name="Basic", base_price=10)

    def test_calculate_quote_price(self):
        price = calculate_quote_price(self.product, 5)
        self.assertEqual(price, 50.0)

    def test_create_quote_via_view(self):
        response = self.client.get(reverse("new_quote"))
        self.assertEqual(response.status_code, 200)

        data = {
            "branch": self.branch.id,
            "product": self.product.id,
            "subscriber_name": "John Doe",
            "start_date": "2024-01-01",
            "duration": 3,
        }
        response = self.client.post(reverse("new_quote"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Quote.objects.exists())
