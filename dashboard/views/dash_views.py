""" View function for the main portfolio dashbaord app """
import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from dashboard.models import Stock, Trade, Portfolio
from dashboard.forms import PortfolioForm
from dashboard.iex_requests import list_symbols
from dashboard.utils import context_assign_user

logger = logging.getLogger(__name__)

@login_required(login_url='/dash/login/')
def index(request):
	""" The home dashboard view """
	context = context_assign_user(request.user)
	logger.info('loading portfolio index %{user.username}')
	if request.method == 'POST':
		form = PortfolioForm(request.POST)
		if form.is_valid():
			Portfolio.objects.filter(user_profile=context['current_user']).update(name=request.POST['name'], benchmark_name=request.POST['benchmark_name'], benchmark_ticker=request.POST['benchmark_ticker'])
			messages.success(request, 'Congrats, Your portfolio was updated!')
			return redirect('dash:dashboard')
	portfolio = Portfolio.objects.filter(user_profile=context['current_user']).first()
	context['stocks'] = portfolio.get_current_quotes()
	context['latest'] = portfolio.latest_day_data(context['stocks'])
	context['symbols'] = list_symbols()
	context['portfolio'] = portfolio
	context['portfolio_form'] = PortfolioForm()
	return render(request, 'dash/dashboard.html', context)


@login_required(login_url='/dash/login/')
def stock(request, stock_uuid):
	""" Stock view """
	context = context_assign_user(request.user)
	stock_object = get_object_or_404(Stock, uuid=stock_uuid)
	other_stocks = Stock.objects.filter(user_profile=context['current_user'], status='a').exclude(pk=stock_object.id)
	context['stock'] = stock_object
	context['trades'] = stock_object.trades()
	context['stocks'] = other_stocks
	context['price_data'] = json.dumps(stock_object.ticker_data.historical_data)
	return render(request, 'dash/stock_detail.html', context)

@login_required(login_url='/dash/login/')
def trades(request, stock_uuid):
	return HttpResponse("You're looking at trades for %s." % stock_uuid)

@login_required(login_url='/dash/login/')
def trade(request, trade_uuid):
	trade_object = get_object_or_404(Trade, uuid=trade_uuid)
	return render(request, 'dash/trade.html')
