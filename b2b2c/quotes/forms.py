from django import forms

from .models import Branch, Product, Quote, Option


class QuoteForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)
    options = forms.ModelMultipleChoiceField(
        queryset=Option.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Quote
        fields = [
            "branch",
            "product",
            "subscriber_name",
            "start_date",
            "duration",
            "options",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.none()
        if "branch" in self.data:
            try:
                branch_id = int(self.data.get("branch"))
                self.fields["product"].queryset = Product.objects.filter(branch_id=branch_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["product"].queryset = Product.objects.filter(branch=self.instance.product.branch)

        if "product" in self.data:
            try:
                product_id = int(self.data.get("product"))
                self.fields["options"].queryset = Option.objects.filter(product_id=product_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["options"].queryset = Option.objects.filter(product=self.instance.product)

