from django import forms
from django.core.exceptions import ValidationError

from FullStackApp.models import ShippingRegion, User


class CartProduct(forms.Form):
    pass


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    # name = forms.CharField(max_length=100)
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=1, widget=forms.HiddenInput)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartUpdateProductForm(CartAddProductForm):
    def __init__(self, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.fields['quantity'].hidden_widget = False


class CustomerOrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    company = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    country = forms.ModelChoiceField(queryset=ShippingRegion.objects.filter(),
                                     widget=forms.Select(attrs={'class': 'dropdown_item_select checkout_input'}),
                                     empty_label=None)
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    address_2 = forms.CharField(max_length=100, required=False,
                                widget=forms.TextInput(attrs={'class': 'checkout_input checkout_address_2'}))
    zipcode = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    phone_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'checkout_input'}))
    accept_terms = forms.BooleanField(initial=False, required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'billing_checkbox'}))
    create_account = forms.BooleanField(required=False, initial=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'billing_checkbox'}))


    def clean_accept_terms(self):
        accept_terms = self.cleaned_data['accept_terms']
        if not accept_terms:
            raise ValidationError('You must Accept our terms and Conditions')
        return accept_terms

    def clean_create_account(self):
        create_account = self.cleaned_data['create_account']
        if not create_account:
            raise ValidationError('You must Click Create Account for your order to be successful')
        return create_account

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email, username=email)
        print(user)
        if user.exists():
            raise ValidationError('Email already exist')
        return email


