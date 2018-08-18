# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.http import Http404
# from django.contrib import messages
# from gas_dash.forms import SignUpForm, StockForm
# from gas_dash.models import Stock, Trade
# from gas_dash.iex_requests import *


# @login_required(login_url='/gas_dash/login/')
# def index(request):
# 	""" The home dashboards view """
# 	current_user = request.user
# 	profile = current_user.profile
# 	stocks = Stock.objects.filter(user_profile=profile)
# 	context = {'stocks': stocks}
# 	return render(request, 'gas_dash/dashboard.html', context)


# @login_required(login_url='/gas_dash/login/')
# def stock(request, stock_id):
# 	stock = get_object_or_404(Stock, pk=stock_id)
# 	stock_data = stock_profile(stock.ticker)
# 	stock_data['stock'] = stock
# 	return render(request, 'gas_dash/stock_detail.html', {'stock_data': stock_data})

# @login_required(login_url='/gas_dash/login/')
# def trades(request, stock_id):
# 	return HttpResponse("You're looking at trades for %s." % stock_id)

# @login_required(login_url='/gas_dash/login/')
# def trade(request, trade_id):
# 	stocks = Stock.objects.all()
# 	return HttpResponse("You're looking at trade %s." % trade_id)
