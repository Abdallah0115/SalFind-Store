from .forms import CustForm, searchForm, editCustForm, UserPasswordUpdateForm
from django.contrib.auth.hashers import make_password, check_password
from .models import Item, Cust, order, ItemRate, Coupon, CouponUser, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg ,Q
from django.utils import timezone
from django.conf import settings
import plotly.graph_objs as go
import plotly.offline as opy
import joblib as job
import pandas as pd
import numpy as np
import datetime
import random
import string
import os

# Create your views here.

def Welcome(req):

    item = Category.objects.filter()

    return render(req,'welcome.html',{"items":item})

def Login(req):

    try:
        if req.method == 'POST':

            username = req.POST.get('username')

            password = req.POST.get('password')

            user = authenticate(req, username=username, password=password) 

            cu = Cust.objects.get(email = req.POST.get('username'))

            if (user and cu):

                login(req, user)

                return redirect('/SalFind/Market/0')

            else:

                return render(req, 'cusLogin.html', {'error': 'Invalid username or password'})

        return render(req, 'cusLogin.html')
    except:
        return render(req, 'cusLogin.html', {'error': 'Invalid username or password'})

def Emailenter(req):
    if(req.method == "POST"):
        if(req.POST.get("Custmail")):

            va = searchForm(req.POST)

            if(va.is_valid()):
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                hashCode = make_password(code)
                subject = 'SaleFind store Coupone !'
                message = f"we gona check that it's yor email the verification code is {code}"
                sender = 'SalFind@gmail.com'
                recipient_list = [req.POST.get("Custmail")]
                send_mail(subject, message, sender, recipient_list,fail_silently=False)
                req.session["username"] = req.POST.get("Custmail")
                req.session["code"] = hashCode
                return redirect("/SalFind/Valid")

            else:

                return render(req ,"emailValid.html" ,{"Error":"NOT VALID !"})

    else:
        return render(req ,"emailValid.html")
    
    return render(req ,"emailValid.html")

def validation(req ):
    if(req.method == "POST"):
        
        if(req.POST.get("CustValid")):
            if(check_password(req.POST.get("CustValid"),req.session.get("code"))):
                return redirect("/SalFind/sign")
            else:
                return render(req,"valid.html" ,{"Error":"NOT VALID !"})
    else:
        return render(req,"valid.html" )
    
    return render(req,"valid.html" )

def Sign(req):

    if(req.method == "POST"):

        form = CustForm(req.POST , req.FILES)

        if(form.is_valid()):

            form.save()

            return redirect('/SalFind/login')

    else:

        form = CustForm()

    return render(req,'sign.html',{'form':form , "email":req.session.get("username")})

User = get_user_model()

@login_required
def Market(req,id):

    use = get_object_or_404(Cust,email= req.user.username)

    if(req.method == "POST"):

            query = req.POST.get('search')

            if query:

                items =  Item.objects.filter(  
                                                Q(sku__icontains=query) |
                                                Q(Category__name__icontains=query),
                                                is_Active=True
                                                ).annotate(average_rating=Avg('itemrate__rate'))
            else:

                items = Item.objects.all()

            return render(req, 'Market.html', {'items': items[:20],'user':use})

    else:

        top_items = (ItemRate.objects
            .values('item__sku', 'item__price', 'item__Category','item__discAv','item__image')
            .annotate(avg_rate=Avg('rate'))
            .order_by('avg_rate')[:100])

        start = id * 20 
        end = start + 20

        return render(req ,'Market.html' ,{'items' : top_items[start:end] ,'user':use})

def calculate_average_rate(item_id):
    
    average_rate = ItemRate.objects.filter(item_id=item_id).aggregate(avg_rate=Avg('rate'))
    return average_rate['avg_rate'] if average_rate['avg_rate'] is not None else 0

def gen_encode(x):

    if(x == "F"):

        return 0

    elif(x=="M"):

        return 1

def age_encode(x):

    if(x == "youth"):

        return 0

    elif(x=="middle"):

        return 1

    elif(x=="old"):

        return 2

def map_age_to_group(age):

    if( 0 < age and age <=18 ):
        return "youth"
    elif(18 < age and age <=40):
        return "middle"
    else:
        return "old"

def cluster( cat , pay , value , customer):
    # category encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codCat.pkl'))
    cate = job.load(path1)
    data = [cat.name]
    category = cate.transform(data)

    # Gender encode
    gender_enc = gen_encode( customer.gender)

    # payment method encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codPayment.pkl'))
    payM = job.load(path1)
    pay_encoded = payM.transform([pay])

    # state encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codState.pkl'))
    state = job.load(path1)
    state_encoded = state.transform([customer.state])

    # age encoded
    ageLa = map_age_to_group(customer.age)
    age_group_enc = age_encode(ageLa)

    # date encoded
    month = datetime.datetime.now().month

    # cluster
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'modCluster.pkl'))
    cluster = job.load(path1)
    group_enc = cluster.predict([[category[0],
                                gender_enc,
                                pay_encoded[0],
                                state_encoded[0],
                                age_group_enc,
                                month,
                                value]])
    return group_enc

def discV( cat , pay , value , customer):
    #'category_enc', 'gender_enc','pay_encoded', 'state_encoded', 'age_group_enc','month','group_enc'

    # category encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codCat.pkl'))
    cate = job.load(path1)
    data = [cat.name]
    category = cate.transform(data)

    # Gender encode
    gender_enc = gen_encode( customer.gender)

    # payment method encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codPayment.pkl'))
    payM = job.load(path1)
    pay_encoded = payM.transform([pay])

    # state encoder
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'codState.pkl'))
    state = job.load(path1)
    state_encoded = state.transform([customer.state])

    # age encoded
    ageLa = map_age_to_group(customer.age)
    age_group_enc = age_encode(ageLa)

    # date encoded
    month = datetime.datetime.now().month

    # cluster
    path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'modCluster.pkl'))
    cluster = job.load(path1)
    group_enc = cluster.predict([[category[0],
                                gender_enc,
                                pay_encoded[0],
                                state_encoded[0],
                                age_group_enc,
                                month,
                                value]])

    #data
    data = [category[0],
            gender_enc,
            pay_encoded[0],
            state_encoded[0],
            age_group_enc,
            month,
            group_enc[0]]

    if(value > 15000 ):
        return True
    else:

        #decition tree
        path1 = os.path.join(os.path.join(settings.CSV_DATA_DIR, 'modClass.pkl'))
        modelLog = job.load(path1)
        bol = modelLog.predict([data])[0]

    with open("MyFile.txt", "a") as file:
    # Append your content
        file.write(f"{bol}\n")

    return bol

@login_required
def item(req,sk):

    use = get_object_or_404(Cust,email= req.user.username)

    It = Item.objects.get(sku=sk)

    rate = calculate_average_rate(sk)

    obj = ItemRate.objects.filter(cust = use,item=It )

    if(It is not None):

        if(req.method == "POST"):

            mess = None

            userN = Cust.objects.get(username = req.user.username)

            if(req.POST.get("rate")):
                temp = ItemRate.objects.create(cust = use , item = It , rate = req.POST.get("rate"))

            if(req.POST.get("quantity") and req.POST.get("payM")):

                rate = calculate_average_rate(sk)

                qt = req.POST.get("quantity")

                total = It.price * int(qt)

                newTotal = total

                if(discV(It.Category, req.POST.get("payM"), total , userN) or It.discAv):


                    group_enc = cluster(It.Category, req.POST.get("payM"), total , userN)
                    if(group_enc == 0):
                        file_path = os.path.join(settings.CSV_DATA_DIR, 'modRegOne.pkl')

                        path = os.path.join(file_path)

                        model = job.load(path)

                        data = np.array([total , qt]).reshape(1, -1)

                        newTotal = model.predict(data)[0]

                    elif(group_enc == 1):
                        file_path = os.path.join(settings.CSV_DATA_DIR, 'modRegTwo.pkl')

                        path = os.path.join(file_path)

                        model = job.load(path)

                        data = np.array([total , qt]).reshape(1, -1)

                        newTotal = model.predict(data)[0]

                    if(newTotal > total):
                        newTotal = .94 * float( total)

                    newTotal = np.floor(newTotal)

                if(req.POST.get("cop")):

                    coupon_exists = Coupon.objects.filter(code= req.POST.get("cop")).exists()

                    if coupon_exists:
                        cop = Coupon.objects.get(code = req.POST.get("cop"))

                        if(cop.is_active and cop.valid_to > timezone.now().date()):
                            newTotal = (1 - float(cop.discount_value)) * newTotal

                        else:

                            mess = "not valid coupon !"

                return render(req,
                                'offer.html',
                                {'It' : It ,
                                    'rate' : rate,
                                    'newT' : newTotal,
                                    'oldT' : total, 
                                    'payM': req.POST.get("payM"),
                                    'qt' : req.POST.get("quantity"),
                                    'code':req.POST.get("cop"),
                                    'messege':mess,
                                    'user':use,
                                    'rate':rate
                                }
                            )

        else:

            if(obj):

                return render(req,'item.html',{'It' : It , 'rate' : rate ,'user':use})
            
            else:

                return render(req,'item.html',{'It' : It , 'user':use})

@login_required
def offer(req , item):
    
    try:

        if(req.method == "POST"):

            It = Item.objects.get(sku=item)

            if(It is not None):

                userN = Cust.objects.get(username = req.user.username)

                status1 = "complete"

                qt = req.POST.get("quantity")

                value1 = It.price * int(qt)

                newTotal = value1

                discount_per = 0

                if(discV(It.Category, req.POST.get("payMethod"), value1 , userN) or It.discAv):

                    group_enc = cluster(It.Category, req.POST.get("payMethod"), value1 , userN) 

                    if(group_enc == 0):
                        file_path = os.path.join(settings.CSV_DATA_DIR, 'modRegOne.pkl')

                        path = os.path.join(file_path)

                        model = job.load(path)

                        data = np.array([value1 , qt]).reshape(1, -1)

                        newTotal = model.predict(data)[0]

                    elif(group_enc == 1):
                        file_path = os.path.join(settings.CSV_DATA_DIR, 'modRegTwo.pkl')

                        path = os.path.join(file_path)

                        model = job.load(path)

                        data = np.array([value1 , qt]).reshape(1, -1)

                        newTotal = model.predict(data)[0]

                    newTotal = np.floor(newTotal)

                if(req.POST.get("cop")):

                    coupon_exists = Coupon.objects.filter(code= req.POST.get("cop")).exists()

                    if coupon_exists:
                        cop = Coupon.objects.get(code = req.POST.get("cop"))

                        if(cop.is_active and cop.valid_to > timezone.now().date()):
                            newTotal = (1 - float(cop.discount_value)) * newTotal

                            CouponUser.objects.create(
                                                        user_id = userN,

                                                        Coupon_id = cop
                                                    )

                discount_am =  float(value1) - float(newTotal)

                discount_per = discount_am / float(value1)

                if (req.POST.get("payMethod") == "cod"):
                    status1 = "cod"

                order.objects.create(user =userN,
                                        status = status1,
                                        value = value1,
                                        discount_amount = discount_am,
                                        total = newTotal,
                                        payment_method = req.POST.get("payMethod"),
                                        qty_ordered = qt,
                                        item = It,
                                        discout_percentage = discount_per
                                        )

                return render(req,'succes.html')

            else:

                return render(req,'failed.html')

        else:

            return render(req,'failed.html')

    except:

        return render(req,'failed.html')

def userGraph(user):
    orders = order.objects.exclude(status="canceled")

    orders = orders.filter(user = user)

    order_dates = [order.order_date for order in orders]
    totals = [order.total for order in orders]

    trace = go.Scatter(x = order_dates, y = totals, mode='lines', name='Total Amount')
    layout = go.Layout(title='Total Amount Over Time',
                        xaxis=dict(title='Order Date'),
                        yaxis=dict(title='Total Amount'))

    fig = go.Figure(data=[trace], layout=layout)

    # Convert the Plotly figure to HTML
    chart_html = opy.plot(fig, auto_open=False, output_type='div')

    return chart_html

@login_required
def profile(req,person):

    try:

        man = get_object_or_404(Cust,email = person)

        complete = order.objects.filter(user = man,status = "complete")

        cod = order.objects.filter(user = man ,status = "cod")

        refund = order.objects.filter(user = man ,status = "refund")

        recived = order.objects.filter(user = man ,status = "recieved")

        current_date = timezone.now()

        # Calculate the date 14 days ago
        date_14_days_ago = current_date - timezone.timedelta(days=14)

        recived = recived.filter(order_date__gte=date_14_days_ago)

        graph = userGraph(man)

        return render(req,'profile.html',{'user':man,'rec':recived ,'com':complete , 'cod' :cod ,'ref':refund ,'chart':graph})

    except:

        return redirect("/SalFind/Market/0")

@login_required
def Refund(req,id):
    user = req.user.username
    try:

        obj = get_object_or_404(order,id = id)

        obj.status = "refund"

        obj.save()

        return redirect(f"/SalFind/me/{user}")

    except:

        return redirect(f"/SalFind/me/{user}")

@login_required
def cancel(req,id):
    user = req.user.username
    try:

        obj = get_object_or_404(order,id = id)

        obj.status = "canceled"

        obj.save()

        return redirect(f"/SalFind/me/{user}")

    except:

        return redirect(f"/SalFind/me/{user}")

@login_required
def edit_profile(req):
    try:

        obj = get_object_or_404( Cust , email = req.user.username)

        if(req.method == "POST"):
            
            data = editCustForm(req.POST , req.FILES , instance= obj)

            if(data.is_valid()):

                data.save()

                return redirect(f"/SalFind/me/{req.user.username}")

        else:

            form = editCustForm(instance = obj)

        return render(req,'sign.html',{"form":form})

    except:

        return redirect(f"/SalFind/me/{req.user.username}")

def Logout_view(request):
    
    logout(request)

    return redirect('SalFind')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('/SalFind/login')
    else:
        form = UserPasswordUpdateForm(request.user)
    return render(request, 'changePass.html', {'form': form})