""" Views for the sites forms """
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.utils import context_assign_user
from dashboard.forms import StockForm, TradeForm
from dashboard.models import Ticker

@login_required(login_url='/dash/login/')
def add_stock(request):
	""" Function for adding a new stock to the dashboard: limited to stocks on IEX """
	context = context_assign_user(request.user)
	if request.method == 'POST':
		# Create form instance and populate with data from request
		form = StockForm(request.POST)
		if form.is_valid():
			stock = form.save(commit=False)
			stock.user_profile_id = request.user.profile.id
			stock.ticker = stock.ticker_data.ticker
			stock.save()
			messages.success(request, 'Congrats, Your stock was added!')
			return redirect('dash:dashboard')
		errors = form.errors
		form = StockForm(request, request.POST)
		messages.warning(request, "There's a problem with the form")
	context['symbols'] = [{'data': stock.id, 'value': stock.name} for stock in Ticker.objects.all()]
	context['stock_form'] = StockForm()
	return render(request, 'dash/add_stock.html', context)

@login_required(login_url='/dash/login/')
def add_trade(request):
	""" Function adds a trade for a users stock to the db """
	context = context_assign_user(request.user)
	if request.method == 'POST':
		# Create form instance and populate with data from reqquest
		form = TradeForm(request, request.POST)
		if form.is_valid():
			trade = form.save(commit=False)
			d = datetime.strptime(request.POST['date'], '%d/%m/%Y').date()
			trade.date = d
			trade.save()
			messages.success(request, 'Congrats, Your trade was added!')
			return redirect('dash:dashboard')
		errors = form.errors
		trade_form = TradeForm(request, request.POST)
		messages.warning(request, "There's a problem with the form")
		return render(request, 'dash/add_trade.html', {'form': trade_form, 'errors': errors})
	context['trade_form'] = TradeForm(request)
	return render(request, 'dash/add_trade.html', context)
