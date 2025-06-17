from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import QuoteForm
from .models import Branch, Product, Quote


def new_quote(request):
    form = QuoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        quote = form.save(commit=False)
        quote.price = calculate_quote_price(quote.product, quote.duration)
        quote.save()
        return redirect("quote_detail", quote_id=quote.pk)

    return render(request, "quotes/new_quote.html", {"form": form})


def load_products(request):
    branch_id = request.GET.get("branch")
    products = Product.objects.filter(branch_id=branch_id)
    return render(request, "quotes/product_options.html", {"products": products})


def quote_price(request):
    product_id = request.GET.get("product")
    duration = int(request.GET.get("duration", 0))
    price = ""
    if product_id and duration:
        try:
            product = Product.objects.get(pk=product_id)
            price = calculate_quote_price(product, duration)
        except Product.DoesNotExist:
            price = ""
    return render(request, "quotes/price.html", {"price": price})


def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    return render(request, "quotes/quote_detail.html", {"quote": quote})


def calculate_quote_price(product: Product, duration: int) -> float:
    return float(product.base_price) * duration
