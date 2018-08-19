from django.urls import path, re_path

from .views import dash_views, registration_views, form_views
from django.contrib.auth import views as auth_views 

app_name = 'dash'
urlpatterns = [
	# This is the home dashboard '/gas_dash'
    path('', dash_views.index, name='index'),
    # The registration view
    re_path(r'^signup/$', registration_views.signup, name='signup'),
    # This is the login page
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    # The logout page
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'},  name='logout'),
    # Add a stock
    path('stocks/add', form_views.add_stock, name='add_stock'),
    # Add a trade
    path('trade/add', form_views.add_trade, name='add_trade'),
    # This is a stock page '/gas_dash/<stock_id>'
    path('stocks/<int:stock_id>', dash_views.stock, name='stock'),
    # This is a stock trades page '/gas_dash/<stock_id>/trades'
    path('stocks/<int:stock_id>/trades', dash_views.trades, name='trades'),
    # This is a trade page '/gas_dash/<trade_id>'
    path('trade/<int:trade_id>', dash_views.trade, name='trade')
]
