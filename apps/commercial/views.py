from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages

from apps.base.models import *
from apps.base.forms import *

def commercial(request, place_id=None):
	places = Place.objects.all()
	if not place_id and places:
		return redirect ('commercial', place_id=places[0].id)
	else:
		tables = Table.objects.filter(place=place_id)
	return render(request, 'commercial/index.html', locals())
	
def payer(request, table_id):
	table = Table.objects.get(id=table_id)
	commandes = Commande.objects.filter(table=table_id, reste__gt=0)
	a_payer = commandes.aggregate(Sum('reste'))['reste__sum']
	return render(request, 'commercial/payement.html', locals())
	
def stock(request):
	places = Place.objects.all()
	products = Produit.objects.all()
	return render(request, 'commercial/stock.html', locals())
	
def requisition(request):
	requisitions = Stock.objects.filter(is_valid=False, quantite__lt=0)
	return render(request, 'commercial/requisition.html', locals())
	
def achats(request, product_id):
	achat_form = StockForm(product_id, request.POST)
	if request.method == "POST":
		if achat_form.is_valid():
			stock = achat_form.save(commit=False)
			stock.personnel = request.user.personnel
			stock.produit = Produit.objects.get(id = product_id)
			stock.save()
			messages.success(request, "approvisionnement effectuée")
	achat_form = StockForm(product_id)
	return render(request, 'commercial/form.html', locals())
	
def offre(request, product_id):
	offre_form = OffreForm(request.POST)
	if request.method == "POST":
		if offre_form.is_valid():
			offre = offre_form.save(commit=False)
			offre.produit = Produit.objects.get(id = product_id)
			offre.save()
			messages.success(request, "offre ajoutée avec succes")
	offre_form = OffreForm()
	return render(request, 'commercial/form.html', locals())

def details(request, product_id):
	stocks = Stock.objects.filter(produit = product_id)
	return render(request, 'commercial/details.html', locals())

def tables(request):
	return render(request, '404.html', locals())
	

