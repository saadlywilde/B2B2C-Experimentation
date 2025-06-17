from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import QuoteForm
from .models import Branch, Product, Quote, Option


def new_quote(request):
    form = QuoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        quote = form.save(commit=False)
        options = form.cleaned_data.get("options")
        quote.price = calculate_quote_price(quote.product, quote.duration, options)
        quote.save()
        form.save_m2m()
        return redirect("quote_detail", quote_id=quote.pk)

    return render(request, "quotes/new_quote.html", {"form": form})


def load_products(request):
    branch_id = request.GET.get("branch")
    products = Product.objects.filter(branch_id=branch_id)
    return render(request, "quotes/product_options.html", {"products": products})


def load_options(request):
    product_id = request.GET.get("product")
    options = Option.objects.filter(product_id=product_id)
    return render(request, "quotes/option_checkboxes.html", {"options": options})


def quote_price(request):
    product_id = request.GET.get("product")
    duration = int(request.GET.get("duration", 0))
    option_ids = request.GET.getlist("options")
    price = ""
    if product_id and duration:
        try:
            product = Product.objects.get(pk=product_id)
            options = Option.objects.filter(id__in=option_ids)
            price = calculate_quote_price(product, duration, options)
        except Product.DoesNotExist:
            price = ""
    return render(request, "quotes/price.html", {"price": price})


def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    return render(request, "quotes/quote_detail.html", {"quote": quote})


def calculate_quote_price(product: Product, duration: int, options=None) -> float:
    base = float(product.base_price) * duration
    extras = 0.0
    if options:
        extras = sum(float(opt.price) for opt in options)
    return base + extras
