from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from datetime import datetime
from dashboard.models import Stock, Trade
from dashboard.forms import SignUpForm, StockForm, TradeForm
from dashboard.iex_requests import *
from dashboard.stock_functions import recalc_stock


@login_required(login_url='/dash/login/')
def add_stock(request):
	""" Function for adding a new stock to the dashboard: limited to stocks on IEX """
	if request.method == 'POST':
		# Create form instance and populate with data from request
		form = StockForm(request.POST)
		if form.is_valid():
			stock = form.save(commit=False)
			stock.user_profile_id = request.user.profile.id
			stock.save()
			messages.success(request, 'Congrats, Your stock was added!')
			return redirect('dash:index')
	symbols = list_symbols()
	current_user = request.user
	profile = current_user.profile
	stock_form = StockForm()
	return render(request, 'dash/add_stock.html', {'form': stock_form, 'symbols': symbols})

@login_required(login_url='/dash/login/')
def add_trade(request):
	""" Function adds a trade for a users stock to the db """
	if request.method == 'POST':
		# Create form instance and populate with data from reqquest
		form = TradeForm(request, request.POST)
		print(request.POST['date'])
		if form.is_valid():
			trade = form.save(commit=False)
			d = datetime.strptime(request.POST['date'], '%d/%m/%Y').date()
			trade.date = d
			trade.save()
			messages.success(request, 'Congrats, Your trade was added!')
			recalc_stock(trade.stock_id)
			return redirect('dash:index')
		else:
			errors = form.errors
			trade_form = TradeForm(request, request.POST)
			messages.warning(request, "There's a problem with the form")
			return render(request, 'dash/add_trade.html', { 'form': trade_form, 'errors': errors })	
	trade_form = TradeForm(request)
	return render(request, 'dash/add_trade.html', { 'form': trade_form })
