""" URL management for dashboard app """
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from dashboard.views import form_views, dash_views, registration_views
from dashboard.views.users import profile_views
from gas_dash import settings

app_name = 'dash'
urlpatterns = [
    # This is the home dashboard '/gas_dash'
    path('', dash_views.index, name='dashboard'),
    # The registration view
    re_path(r'^signup/$', registration_views.signup, name='signup'),
    # This is the login page
    re_path(r'^login/$', registration_views.login_view, name='login'),
    # The logout page
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},  name='logout'),
    ### Users views ###
    # Ajax set menu status
    re_path(r'^set_menu_status_closed', profile_views.update_menu_session),
    re_path(r'^set_menu_status_open', profile_views.update_menu_session),
    ### Stock URLs ###
    # Add a stock
    path('stocks/add', form_views.add_stock, name='add_stock'),
    # Add a trade
    path('trade/add', form_views.add_trade, name='add_trade'),
    # This is a stock page '/dash/<stock_id>'
    path('stocks/<uuid:stock_uuid>', dash_views.stock, name='stock'),
    # AJAX request ticker update
    path('ticker/request_update/<uuid:ticker_uuid>', dash_views.fill_ticker_data),
    # This is a stock trades page '/gas_dash/<stock_id>/trades'
    path('stocks/<uuid:stock_uuid>/trades', dash_views.trades, name='trades'),
    # This is a trade page '/gas_dash/<trade_id>'
    path('trade/<uuid:trade_uuid>', dash_views.trade, name='trade'),
    ### User URLs ###
    path('show_profile/<uuid:profile_uuid>', profile_views.show_profile, name='profile')
]
