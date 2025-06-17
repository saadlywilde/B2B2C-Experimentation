from django import forms

from .models import Branch, Product, Quote


class QuoteForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)

    class Meta:
        model = Quote
        fields = ["branch", "product", "subscriber_name", "start_date", "duration"]
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
