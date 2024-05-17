import re
from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", phone):
            raise forms.ValidationError("Неверный формат номера телефона. Формат должен быть: +7 (XXX) XXX-XX-XX")
        return phone
