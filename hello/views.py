from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect


from .models import Product2
from .forms import OrderForm
from hello.models import Order

# Create your views here.
def index(request):
    return render(request, 'index.html', {'pizza_list': Product2.objects.all()})

#function getting list of order excluding ones without date, sortedy by date
def getAllOrders(request):
    order_list = Order.objects.exclude(createdDate=None).order_by('-createdDate')
    return render(request, 'orderHistory.html', {'orderList': order_list})

def thank(request, order):
    return render(request, 'thank.html', {'order': order})

def products(request):
    return render(request, 'products.html')


#method which pulls out user input data from form. Then object is saved in the postgres database and returned by method
def createOrder(form, product):
    order = Order(
        name=form.cleaned_data['customerName'],
        surname=form.cleaned_data['customerSurname'],
        postalcode=form.cleaned_data['customerPostalCode'],
        city=form.cleaned_data['customerCity'],
        street=form.cleaned_data['customerStreet'],
        phone=form.cleaned_data['customerPhone'],
        email=form.cleaned_data['customerEmail'],
        product=product)
    order.save()
    return order

def checkout(request, id):
    # if this is a POST request we need to process the form data
    instance = get_object_or_404(Product2, id=id)
    Context = {
        "id": instance.id,
        "instance": instance
    }
    product = Product2.objects.get(id=id)


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OrderForm(request.POST)

    # check whether it's valid:
        if form.is_valid():
            order = createOrder(form, product)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return thank(request, order)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'instance': Context})