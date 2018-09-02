from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from dashboard.models import Stock, Trade
from dashboard.iex_requests import *
from dashboard.stock_functions import get_current_quotes
from dashboard.dash_functions import portfolio_data


@login_required(login_url='/dash/login/')
def index(request):
	""" The home dashboards view """
	current_user = request.user
	profile = current_user.profile
	stocks = Stock.objects.filter(user_profile=profile, status='a')
	stocks = get_current_quotes(stocks)
	context = {'stocks': stocks}
	return render(request, 'dash/dashboard.html', context)


@login_required(login_url='/dash/login/')
def stock(request, stock_id):
	stock = get_object_or_404(Stock, pk=stock_id)
	stock_data = stock_profile(stock.ticker)
	other_stocks = Stock.objects.filter(user_profile=request.user.profile, status='a').exclude(pk=stock_id)
	stock_data['stock'] = stock
	stock_data['trades'] = stock.trades()
	stock_data['stocks'] = other_stocks
	return render(request, 'dash/stock_detail.html', {'stock_data': stock_data})

@login_required(login_url='/dash/login/')
def trades(request, stock_id):
	return HttpResponse("You're looking at trades for %s." % stock_id)

@login_required(login_url='/dash/login/')
def trade(request, trade_id):
	trade = get_object_or_404(Trade, pk=trade_id)
	return render(request, 'dash/trade.html')
