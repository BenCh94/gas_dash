""" Form objects used in dashboard app """
from django import forms
from django.forms import ModelForm, TextInput, DateInput, PasswordInput, CheckboxInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from dashboard.models import Stock, Trade, Portfolio, Profile


class SignUpForm(UserCreationForm):
    """ New user sign up form """
    username = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254, help_text='A valid email address is required.')
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput, label=' Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username', 'id': 'register_username', 'class': 'sleek_input'})
        self.fields['email'].widget = TextInput(attrs={'placeholder': 'E-mail', 'id': 'register_email', 'class': 'sleek_input'})
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password', 'id': 'register_password1', 'class': 'sleek_input'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'register_password2', 'class': 'sleek_input'})


class LoginForm(AuthenticationForm):
    """ user login form """
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username', 'id': 'login_username', 'class': 'sleek_input'})
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password', 'id': 'login_password', 'class': 'sleek_input'})


class StockForm(ModelForm):
    """ Add new stock form """
    class Meta:
        model = Stock
        fields = ('name', 'status', 'ticker_data')

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={
            'id': 'autocompleteName',
            'placeholder': 'Start typing the company name...'
            })
        self.fields['ticker_data'].widget = forms.HiddenInput()


class TradeForm(ModelForm):
    """ Add trade form """

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


class PortfolioForm(ModelForm):
    """ Portfolio settings form """
    class Meta:
        model = Portfolio
        fields = ('name', 'benchmark_object')

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'placeholder': 'Name'})
        self.fields['benchmark_object'].widget = TextInput(attrs={
            'id': 'autocompleteName',
            'placeholder': 'Start typing a fund name...'})

class ProfileForm(ModelForm):
    """ User profile settings """
    class Meta:
        model = Profile
        fields = ('palette', 'bio', 'iex_api_key')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget = TextInput(attrs={
            'placeholder': 'A simple user bio...'})
        self.fields['iex_api_key'].widget = forms.PasswordInput(render_value=True)
