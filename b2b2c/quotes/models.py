from uuid import uuid4

from django.db import models


def generate_quote_number() -> str:
    return uuid4().hex[:10].upper()


class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Option(models.Model):
    """Optional guarantee or add-on that impacts the quote price."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Quote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quote_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=generate_quote_number,
    )
    subscriber_name = models.CharField(max_length=200)
    start_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    options = models.ManyToManyField(Option, blank=True)

    def save(self, *args, **kwargs):
        if not self.quote_number:
            self.quote_number = generate_quote_number()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.quote_number}"
