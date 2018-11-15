from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from dashboard.models import Stock, Trade, Portfolio
from dashboard.forms import PortfolioForm
from dashboard.iex_requests import *
from dashboard.stock_functions import get_current_quotes
from dashboard.dash_functions import update_portfolio


@login_required(login_url='/dash/login/')
def index(request):
	""" The home dashboards view """
	current_user = request.user
	profile = current_user.profile
	stocks = Stock.objects.filter(user_profile=profile, status='a')
	stocks = get_current_quotes(stocks)
	if request.method == 'POST':
		form = PortfolioForm(request.POST)
		if form.is_valid():
			Portfolio.objects.filter(user_profile=profile).update(name=request.POST['name'], benchmark_name=request.POST['benchmark_name'], benchmark_ticker=request.POST['benchmark_ticker'])
			messages.success(request, 'Congrats, Your portfolio was updated!')
			return redirect('dash:dashboard')
	portfolio = Portfolio.objects.filter(user_profile=profile).first()
	portfolio_form = PortfolioForm()
	symbols = list_symbols()
	context = { 'stocks': stocks, 'portfolio': portfolio, 'portfolio_form': portfolio_form, 'symbols': symbols }
	return render(request, 'dash/dashboard.html', context)


@login_required(login_url='/dash/login/')
def stock(request, stock_id):
	""" Stock view """
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
