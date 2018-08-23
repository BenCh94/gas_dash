from django import forms
from django.forms import ModelForm, TextInput, ModelChoiceField, DateInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from gas_dash import settings
from .models import Stock, Trade


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254, help_text='A valid email address is required.')
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=' Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password' )


class StockForm(ModelForm):
	class Meta:
		model = Stock
		fields = ('name', 'status', 'ticker')

	def __init__(self, *args, **kwargs):
		super(StockForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget = TextInput(attrs={
			'id': 'autocompleteName',
			'placeholder': 'Start typing the company name...'
			})
		self.fields['ticker'].widget = forms.HiddenInput()


class TradeForm(ModelForm):

	class Meta:
		model = Trade
		fields = ('trade_type', 'stock', 'date','avg_price', 'amount', 'fees_usd')
	def __init__(self, request, *args, **kwargs):
		super(TradeForm, self).__init__(*args, **kwargs)
		current_profile = request.user.profile
		self.fields['stock'].queryset = Stock.objects.filter(user_profile=current_profile)
		self.fields['amount'].widget = TextInput(attrs={
			'placeholder': 'Quantity of the stock...'
			})
		self.fields['avg_price'].widget = TextInput(attrs={
			'placeholder': '$'
			})
		self.fields['fees_usd'].widget = TextInput(attrs={
			'placeholder': '$'
			})
		self.fields['date'].input_formats = ['%d/%m/%Y']
		self.fields['date'].widget = DateInput(attrs={
			'class': 'datepicker',
			'placeholder': 'dd/mm/yyyy'
			}, format='%d/%m/%Y')
