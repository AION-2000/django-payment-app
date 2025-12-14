from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div
 # from django_recaptcha.fields import ReCaptchaField


class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'min': '0.01', 'step': '0.01', 'placeholder': 'Amount'}),
        label="Amount (USD)"
    )
     # captcha = ReCaptchaField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('amount'),
             # Field('captcha'),
            Div(
                Submit('submit', 'Proceed to Payment', css_class='btn btn-primary w-100'),
                css_class='text-center'
            )
        )