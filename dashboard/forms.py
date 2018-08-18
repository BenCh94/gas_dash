from django import forms
from django.forms import ModelForm, TextInput, ModelChoiceField, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Stock, Trade


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )


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
		self.fields['date'].widget = DateInput(attrs={
			'class': 'datepicker',
			'placeholder': 'dd/mm/yyyy'
			}, format='%d/%m/%Y')
