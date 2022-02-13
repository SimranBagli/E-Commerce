from django.shortcuts import render,redirect
from .models import Reviews,Supplier,UserDetail,User,Category,Cart,Location,Deal,Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render,redirect
import stripe
import json
stripe_pub=settings.STRIPE_PUBLISHABLE_KEY
stripe_private=settings.STRIPE_SECRET_KEY

stripe.api_key=stripe_private
# Create your views here.

def home(request):

    try:
        uid = User.objects.get(username=request.user)
        Supplier.objects.get(supplier_username=uid)
        is_valid=True
    except User.DoesNotExist:
        is_valid=False
    except Supplier.DoesNotExist:
        is_valid=False
    tempdata = Supplier.objects.all()
    catdata = Category.objects.all()
    return render(request, 'home.html',{'suppdata':tempdata,'catdata':catdata,'is_valid':is_valid,'location': Location.objects.all()})

def user_logout(request):
    logout(request)
    return  redirect('home')

def showdeal(request,sid):
    try:
        uid = User.objects.get(username=request.user)
        Supplier.objects.get(supplier_username=uid)
        is_valid = True
    except User.DoesNotExist:
        is_valid = False
    except Supplier.DoesNotExist:
        is_valid = False
    uid=User.objects.get(username=sid)
    catdata = Category.objects.all()
    sdata=Supplier.objects.get(supplier_username=sid)

    dealdata=Deal.objects.filter(deal_postedby=uid.id)
    return  render(request,'deals.html',{'dealdata':dealdata,'sdata':sdata,'catdata':catdata,'is_valid':is_valid,'location':Location.objects.all()})

def dealbycat(request,id=None):
    resdata=Supplier.objects.filter(category=id)
    catdata = Category.objects.all()
    try:
        uid = User.objects.get(username=request.user)
        Supplier.objects.get(supplier_username=uid)
        is_valid = True
    except User.DoesNotExist:
        is_valid = False
    except Supplier.DoesNotExist:
        is_valid = False
    return  render(request,'dealbycat.html',{'dealdata':resdata,'catdata':catdata,'is_valid':is_valid,'location':Location.objects.all()})

def supplier_register( request ):
	if request.method == 'POST':
		supplier_name = request.POST.get('supplier_name')
		supplier_email = request.POST.get('supplier_email')
		supplier_password = request.POST.get('supplier_password')
		supplier_username = request.POST.get('supplier_username')
		supplier_address = request.POST.get('supplier_address')
		supplier_contact = request.POST.get('supplier_contact')
		supplier_image1 = request.FILES.get('supplier_image1')
		supplier_image2 = request.FILES.get('supplier_image2')
		supplier_image3 = request.FILES.get('supplier_image3')
		supplier_details = request.POST.get('supplier_details')
		supplier_starttime = request.POST.get('supplier_starttime')
		supplier_endtime = request.POST.get('supplier_endtime')
		location = request.POST.get('location')
		user = User.objects.create_user(supplier_username, supplier_email, supplier_password)
		data = UserDetail(user=user)
		data.save()
		object=Supplier(supplier_name=supplier_name,supplier_email=supplier_email,
						supplier_password=supplier_password,location=Location.objects.get(pk=location),
						supplier_contact=supplier_contact,
						supplier_starttime=supplier_starttime,supplier_endtime=supplier_endtime,
						supplier_username=supplier_username,supplier_address=supplier_address,supplier_image1=supplier_image1,
						supplier_image2=supplier_image2,supplier_image3=supplier_image3,supplier_details=supplier_details,userid=User.objects.get(pk=user.id))
		object.save()
		return redirect('supplier_login')
	else:
		 return render(request, 'supplier_register.html',{'location': Location.objects.all(),'catdata':Category.objects.all()})


def supplier_login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            auth_login(request,user)
            return redirect('supplier_profile')
        else:
            return render(request, 'login.html',
                          {'catdata': Category.objects.all(), 'location': Location.objects.all(),'error':"Invalid Username/Password"})
    else:
        return  render(request,'login.html',{'catdata':Category.objects.all(),'location':Location.objects.all()})


def post_deal( request ):
    if request.method == 'POST':
        deal_title = request.POST.get('deal_title')
        category = request.POST.get('category')
        deal_desc = request.POST.get('deal_desc')
        deal_actualprice = request.POST.get('deal_actualprice')
        deal_price = request.POST.get('deal_price')
        deal_discount = request.POST.get('deal_discount')
        deal_startdate = request.POST.get('deal_startdate')
        deal_enddate = request.POST.get('deal_enddate')
        object=Deal(deal_postedby=User.objects.get(pk=request.user.id),deal_title=deal_title,deal_desc=deal_desc,
					deal_startdate=deal_startdate,deal_enddate=deal_enddate,deal_actualprice=deal_actualprice,deal_price=deal_price,deal_discount=deal_discount,
					category=Category.objects.get(pk=category))
        object.save()

        return redirect('myposteddeals')
    else:
        try:
            uid = User.objects.get(username=request.user)
            Supplier.objects.get(supplier_username=uid)
            is_valid = True
        except User.DoesNotExist:
            is_valid = False
        except Supplier.DoesNotExist:
            is_valid = False
        return render(request, 'postdeal.html',{
            'category':Category.objects.all(),
            'catdata':Category.objects.all(),
            'is_valid':is_valid,
            'location': Location.objects.all()
        })


def edit_deal( request,id ):
    if request.method == 'POST':
        deal_title = request.POST.get('deal_title')
        category = request.POST.get('category')
        deal_desc = request.POST.get('deal_desc')
        deal_actualprice = request.POST.get('deal_actualprice')
        deal_price = request.POST.get('deal_price')
        deal_discount = request.POST.get('deal_discount')
        deal_startdate = request.POST.get('deal_startdate')
        deal_enddate = request.POST.get('deal_enddate')
        obj = Deal.objects.get(pk=id)
        obj.deal_title=deal_title
        obj.deal_desc=deal_desc
        obj.deal_startdate=deal_startdate
        obj.deal_enddate=deal_enddate
        obj.deal_actualprice=deal_actualprice
        obj.deal_price=deal_price
        obj.deal_discount=deal_discount
        obj.category=Category.objects.get(pk=category)

        obj.save()
        return redirect('myposteddeals')
    else:
        dealdata = Deal.objects.get(pk=id)
        try:
            uid = User.objects.get(username=request.user)
            Supplier.objects.get(supplier_username=uid)
            is_valid = True
        except User.DoesNotExist:
            is_valid = False
        except Supplier.DoesNotExist:
            is_valid = False
        return render(request, 'editdeal.html', {
            'category': Category.objects.all(),
            'catdata': Category.objects.all(),
            'deal': dealdata,
            'is_valid':is_valid,
            'location': Location.objects.all()
        })

@login_required(login_url='/login/')
def add_to_cart(request,deal_id):
    if request.method == 'POST':
        user_id=request.user
        deal = Deal.objects.get(pk=deal_id)

        dealdataa = Cart.objects.filter(deal_id=deal_id,user_id=user_id).count()
        if dealdataa>=1:
            dealdata = Cart.objects.get(deal_id=deal_id, user_id=user_id)
            print(dealdata)
            dealdata.quantity = dealdata.quantity+1
            dealdata.total = dealdata.price * dealdata.quantity
            dealdata.save()
            return redirect('cart')
        else:
            price=deal.deal_price
            quantity=1
            total=price*quantity
            object=Cart(user_id=request.user,deal_id=Deal.objects.get(pk=deal_id),price=price,quantity=quantity,total=total)
            object.save()
            return redirect('cart')
    else:
        return  render(request,'home.html',{})

@login_required(login_url='/login/')
def cart(request):
    catdata = Category.objects.all()
    user_id=request.user
    cart = Cart.objects.filter(user_id=user_id)
    total = sum(product.total for product in cart)
    cartdata = []
    for item in cart:
        data = {}
        deal=Deal.objects.get(deal_title=item.deal_id)
        data['deal_id'] =deal.deal_title
        data['description'] = deal.deal_desc
        data['price'] = item.price
        data['quantity'] = item.quantity
        data['total'] = item.total
        data['id'] = item.id
        cartdata.append(data)
    return render(request, 'cart.html', { 'cart': cartdata,'total':total,'catdata': catdata,'key':stripe_pub,'location':Location.objects.all()})

def register(request):
    catdata = Category.objects.all()
    if request.method=='POST':
        username=request.POST.get('username')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        user=User.objects.create_user(username,email,password)
        data=UserDetail(user=user)
        print(username)
        data.save()
        return redirect('user_login')
    else:
        return  render(request,'user_register.html', { 'catdata': catdata,'location':Location.objects.all()})

def user_login(request):
    catdata = Category.objects.all()
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            auth_login(request,user)
            return redirect('uprofile')
        else:
            return render(request, 'ulogin.html', {'catdata': catdata, 'location': Location.objects.all(),'error':'Invalid Username /Password'})
    else:
        return  render(request,'ulogin.html', { 'catdata': catdata,'location':Location.objects.all()})

def cart_delete( request):
    id1 = request.GET.get('id', None)
    Cart.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

@login_required(login_url='/supplier_login/')
def myposteddeals(request):
    try:
        uid = User.objects.get(username=request.user)
        Supplier.objects.get(supplier_username=uid)
        is_valid = True
    except User.DoesNotExist:
        is_valid = False
    except Supplier.DoesNotExist:
        is_valid = False
    uid = request.user
    catdata = Category.objects.all()
    dealdata = Deal.objects.filter(deal_postedby=uid.id)
    return render(request, 'myposteddeals.html', { 'dealdata': dealdata,'catdata': catdata,'is_valid':is_valid,'location':Location.objects.all()})

@login_required(login_url='/login/')
def checkout(request,amount):
   ''' print('Iam in checkpout')
    print(request.POST) '''
   amount=amount
   name='Surbhi'
   address='Phase10 Mohali'
   customer = stripe.Customer.create(
       email=request.POST['stripeEmail'],
       source=request.POST['stripeToken'],
   )
   charge = stripe.Charge.create(
       customer=customer.id,
       amount=amount,
       currency='inr',
       description='donation',
   )
   cart = Cart.objects.filter(user_id=request.user)
   cartdata = {}
   x=0
   for i in cart:
        data = {}
        object = Payment(user_id=request.user, deal_id=i.deal_id, total_amount=charge.amount,
                     payment_amount=i.price,quantity=i.quantity,item_amount=i.total, txn_id=charge.balance_transaction,
                         payment_currency=charge.currency,payment_status=charge.status,
                         payer_email=charge.billing_details.name)
        data['id'] = i.deal_id
        data['amount'] = charge.amount
        data['price'] = i.price
        data['quantity'] = i.quantity
        data['txn_id'] = charge.balance_transaction
        cartdata[x]=data
        x=x+1
        object.save()
   #print(cartdata)
   #print(data)
   subject = 'Deal Purchase Payment'
   fromu = 'snehshine@gmail.com'
   uid = User.objects.get(username=request.user)
   to=uid.email
   j=0
   cartdata1={}
   for i in range(x):
       for x,y in cartdata[i].items():
           cartdata1[x+str(i)]=y

   html_content = render_to_string('mail.html', cartdata1)
   txtmes = render_to_string('mail.html', cartdata1)
   send_mail(subject,txtmes,fromu,[to],fail_silently = False,html_message = html_content)
   cart1 = Cart.objects.filter(user_id=request.user)
   cart1.delete()
   return redirect('paymenthistory')

@login_required(login_url='/login/')
def paymenthistory(request):
    catdata = Category.objects.all()
    paydata = Payment.objects.filter(user_id=request.user)
    return render(request, 'paymenthistory.html', { 'paydata': paydata,'catdata': catdata,'location':Location.objects.all()})

def supplier_profile( request ):
	if request.method == 'POST':
		supplier_name = request.POST.get('supplier_name')
		supplier_email = request.POST.get('supplier_email')
		supplier_password = request.POST.get('supplier_password')
		supplier_username = request.POST.get('supplier_username')
		supplier_address = request.POST.get('supplier_address')
		supplier_contact = request.POST.get('supplier_contact')
		supplier_image1 = request.FILES.get('supplier_image1')
		supplier_image2 = request.FILES.get('supplier_image2')
		supplier_image3 = request.FILES.get('supplier_image3')
		supplier_details = request.POST.get('supplier_details')
		supplier_starttime = request.POST.get('supplier_starttime')
		supplier_endtime = request.POST.get('supplier_endtime')
		location = request.POST.get('location')
		uid = User.objects.get(username=request.user)
		obj = Supplier.objects.get(supplier_username=uid)
		obj.supplier_name=supplier_name
		obj.supplier_email=supplier_email
		obj.location=Location.objects.get(pk=location)
		obj.supplier_contact=supplier_contact
		obj.supplier_starttime=supplier_starttime
		obj.supplier_endtime=supplier_endtime
		obj.supplier_address=supplier_address
		obj.supplier_image1=supplier_image1
		obj.supplier_image2=supplier_image2
		obj.supplier_image3=supplier_image3
		obj.supplier_details=supplier_details
		obj.save()
		return redirect('home')
	else:
            try:
                uid = User.objects.get(username=request.user)
                Supplier.objects.get(supplier_username=uid)
                is_valid = True
            except User.DoesNotExist:
                is_valid = False
            except Supplier.DoesNotExist:
                is_valid = False
            uid = User.objects.get(username=request.user)
            sdata=Supplier.objects.get(supplier_username=uid)
            return render(request, 'supplier_profile.html',{'location': Location.objects.all(),'catdata':Category.objects.all(),"sdata":sdata,'is_valid':is_valid})

@login_required(login_url='/login/')
def change_pass(request):
    if request.method=='POST':
        id=request.user.id;
        data=User.objects.get(pk=id)
        data.set_password(request.POST.get('new_pass1'))
        # data.set_password= request.POST.get('new_pass1')
        data.save()
        #messages.add_message(request,messages.info,'Your password was successfully updated')
        return redirect('home')
    else:
        try:
            uid = User.objects.get(username=request.user)
            Supplier.objects.get(supplier_username=uid)
            is_valid = True
        except User.DoesNotExist:
            is_valid = False
        except Supplier.DoesNotExist:
            is_valid = False
        return  render(request,'changepassword.html',{'is_valid':is_valid,'catdata':Category.objects.all(),'location':Location.objects.all()})

@login_required(login_url='/login/')
def uprofile(request):
    if request.method == 'POST':
        user_info = request.POST.get('user_info')
        user_fname = request.POST.get('user_fname')
        user_lname = request.POST.get('user_lname')
        user_image= request.FILES.get('user_image')
        user_city = request.POST.get('user_city')
        user_phone = request.POST.get('user_phone')
        obj = UserDetail.objects.get(user=request.user.id)
        obj.user_info = user_info
        obj.user_fname = user_fname
        obj.user_lname = user_lname
        obj.user_image = user_image
        obj.user_city = user_city
        obj.user_phone = user_phone
        obj.save()
        return redirect('home')
    else:
        udata = UserDetail.objects.get(user=request.user)
        return render(request, 'profile.html', {'u': udata,'catdata':Category.objects.all(),'location':Location.objects.all()})

def  searchbyloc(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        if location=="--Location--":
            categories=""
        elif location:
            search_items = Supplier.objects.filter(location=location)
            return render(request, 'searchdeal.html', {'dealdata': search_items,'location':Location.objects.all(),'catdata':Category.objects.all()})
        else:
            return render(request, 'searchdeal.html', {'dealdata': {},'location':Location.objects.all(),'catdata':Category.objects.all()})
    else:
        return render(request, 'searchdeal.html', {'dealdata': {},'location':Location.objects.all(),'catdata':Category.objects.all()})

