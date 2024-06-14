from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from Store.models import Cust, Item, ItemRate, Coupon, order
from .forms import ItemForm, ItemEditForm, CouponForm
from django.db.models.functions import Round
from django.db.models import Q ,Avg ,Count
from django.core.mail import send_mail
from generalDash.models import guest
from django.conf import settings
from .Analysis import Analysis
import pandas as pd
import random
import string




def Login(req):
    try:
            if req.method == 'POST':
                username = req.POST.get('username')
                password = req.POST.get('password')
                user = authenticate(req, username = username, password=password)
                cust = Cust.objects.filter(email = username)
                gues = guest.objects.filter(email = username)
                if user is not None and not cust and not gues :
                    login(req, user)

                    return redirect('/dash/hello')
            else:

                return render(req, 'login.html', {'error': 'Invalid username or password'})

            return render(req, 'login.html')
    except:
        return render(req, 'login.html', {'error': 'Invalid username or password'})

@login_required
def hello(req):
    try:
        return render(req,'hello.html',{"user":req.user.username})
    except:
        return redirect('/dash')

@login_required
def Home(req , num):

    try:

        results = order.objects.select_related('item', 'user').values(
                    'order_date',
                    'status',
                    'value',
                    'discount_amount',
                    'total',
                    'payment_method',
                    'discout_percentage',
                    'qty_ordered',
                    'item__sku',
                    'item__Category',
                    'user__full_name',
                    'user__gender',
                    'user__age',
                    'user__county',
                    'user__city',
                    'user__state',
                    'user__user'
                )

        df = pd.DataFrame(list(results))

# Rename the columns as needed
        df = df.rename(columns={
            'order_date':'order_date',
            'status':'status',
            'value':'value',
            'discount_amount':'discount_amount',
            'total':'total',
            'payment_method':'payment_method',
            'discout_percentage':'discount_percentage',
            'qty_ordered':'qty_ordered',
            'item__sku':'sku',
            'item__Category':'category',
            'user__full_name':'full_name',
            'user__gender':'Gender',
            'user__age':'age',
            'user__county':'County',
            'user__city':'City',
            'user__state':'State',
            'user__user':'cust_id'
        })

        charts = Analysis(df)

        if(num == 1):

            user = req.user.username

            total_peices = charts.total_peices()

            total_money = charts.gauge_total()

            chart = charts.total_per_mon()

            total_disc = charts.total_disc()

            total_cust = charts.total_cust()

            return render(req,'home.html' ,{'user':user ,
                                        'peices':total_peices,
                                        'disc':round(total_disc),
                                        'cust':total_cust,
                                        'money':total_money,
                                        'graph':chart})

        elif(num == 2):
            chart = charts.total_Sales_By_Destrib_By_Month()

            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income Per Month"})
    
        elif(num == 3):
            chart = charts.Total_Sales_By_Category()

            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Category"})

        elif(num == 4):

            chart = charts.Total_Sales_By_Gender()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Gender"})
    
        elif(num == 5):

            chart = charts.plot_income_by_age_group()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Age Group"})

        elif(num == 6):

            chart = charts.plot_sales_by_status()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Status"})
    
        elif(num == 7):

            chart = charts.Total_Sales_by_Payment_Method()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Payment Method"})
    
        elif(num == 8):

            chart = charts.Top_10_States_with_Total_Income()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Top 10 States"})
    
        elif(num == 9):

            chart = charts.Low_10_States_with_Total_Income()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Lowest 10 States"})
    
        elif(num == 10):
            chart = charts.Pie_Chart_of_Status_Distribution()
            canceled = charts.canceld()
            ref = charts.ref()
            char = charts.gauge_order_can()
            return render(req , "incom_per_mon.html" ,{"graph":chart ,
                                                    "title":"Orders VS Status",
                                                    "mrD":1,
                                                    "gau":char,
                                                    "can":canceled,
                                                    "Ref":ref})

        elif(num == 11):
            chart = charts.Num_Of_Orders_By_Gendr()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Orders VS Gender"})
    
        elif(num == 12):
            chart = charts.Order_Of_Category()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Orders VS Category"})
    
        elif(num == 13):
            chart = charts.orders_per_state()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Income VS Lowe 10 States"})
    
        elif(num == 14):
            chart = charts.Top_5_Counties_by_Quantity_Ordered()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Top 10 Counties Ordering"})
    
        elif(num == 15):
            chart = charts.Lower_5_Counties_by_Quantity_Ordered()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Lower 10 Counties Ordering"})
    
        elif(num == 16):
            chart = charts.Discount_Percentage_by_Payment_Method()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Discounts VS Payment Method"})
    
        elif(num == 17):
            chart = charts.Average_Discount_Percentage_by_Payment_Method()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Avrage Discounts VS Payment Method"})
    
        elif(num == 18):
            chart = charts.disc_per_month()
            return render(req , "incom_per_mon.html" ,{"graph":chart , "title":"Discounts VS Date"})

        else:

            user = req.user.username

            total_peices = charts.total_peices()

            total_money = charts.gauge_total()

            chart = charts.total_per_mon()

            total_disc = charts.total_disc()

            total_cust = charts.total_cust()

            return render(req,'home.html' ,{'user':user ,
                                        'peices':total_peices,
                                        'disc':round(total_disc),
                                        'cust':total_cust,
                                        'money':total_money,
                                        'graph':chart})

    except:
        return redirect("/dash/hello")

@login_required
def AddItem(req):

    if(req.method == "POST"):

        Mfor = ItemForm(req.POST , req.FILES)

        if(Mfor.is_valid()):

            Mfor.save()

            return redirect('dash/Analysis/1')

    else :

        Rform = ItemForm()

    return render(req, 'addItem.html' , {"form" : Rform})

@login_required
def ManageItem(req):

    try:
        if(req.method == "POST"): 

            query = req.POST.get('search')

            if query:

                items =  Item.objects.filter(  
                                            Q(sku__icontains=query) |
                                            Q(Category__name__icontains=query)
                                            ).annotate(average_rating=Round(Avg('itemrate__rate'),1))

            else:

                items = Item.objects.all()

            return render(req, 'manageItem.html', {'items': items[:20]})

        else:

            top_items = (ItemRate.objects
                .values('item__sku', 'item__price', 'item__Category','item__is_Active')
                .annotate(avg_rate=Avg('rate'))
                .order_by('avg_rate')[:20])

        return render(req ,'manageItem.html' ,{'items' : top_items})
    except:
        return redirect("/dash/hello")

@login_required
def edItem(req , it):

    try:

        item = get_object_or_404(Item ,sku = it)

        if(req.method == "POST"):

            form = ItemEditForm(req.POST,req.FILES ,instance= item)

            if(form.is_valid()):

                form.save()

                return render(req , 'delSuccess.html')

        else:

            form = ItemEditForm(instance=item )

        return render(req,'addItem.html',{'form':form})

    except:

        return render(req , 'edFail.html')

@login_required
def ManageUser(req , num):

    try:
        if(num % 2 == 1):

            top_cust = (
                Cust.objects.annotate(order_count=Count('order__id'))
                .values('order_count', 'name_prefix', 'full_name', 'email', 'state' ,'user__last_login')
                .order_by('-order_count')
            )

            return render(req ,'userManage.html' ,{'items' : top_cust[:20]})
    
        else:

            top_cust = (
                Cust.objects.annotate(order_count=Count('order__id'))
                .values('order_count', 'name_prefix', 'full_name', 'email', 'state' ,'user__last_login')
                .order_by('order_count')
            )

        return render(req ,'userManage.html' ,{'items' : top_cust[:20]})
    except:
        return redirect("/dash/hello")

def generate_coupon_code():

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return code

def is_coupon_code_unique(code):

    return not Coupon.objects.filter(code=code).exists()

def generate_unique_coupon_code():
    code = generate_coupon_code()
    while not is_coupon_code_unique(code):
        code = generate_coupon_code()
    return code

@login_required
def gift(req):
    try:
        co = Coupon.objects.values('code', 'valid_from', 'discount_value' ,'valid_to', 'is_active') \
                                    .annotate(user_count=Count('couponuser__id'))

        return render(req ,'coupon.html' ,{'items' : co})

    except:
        return redirect("/dash/hello")

@login_required
def generatePone(req):

    try:
        if(req.method == "POST"):

            form = CouponForm(req.POST)

            if(form.is_valid()):

                form.save()

                return redirect("/dash/coupon")

        else:

            code = generate_unique_coupon_code()

            form = CouponForm()

        return render(req,'generatCo.html',{"form":form,"code":code})
    except:
        return redirect("/dash/hello")

@login_required
def editPone(req,item):

    try:
        cob = get_object_or_404(Coupon,code = item)

        if(req.method == "POST"):

            form = CouponForm(req.POST,instance = cob)

            if(form.is_valid()):

                form.save()

                return redirect("/dash/coupon")

        else:

            form = CouponForm(instance = cob)

        return render(req,'generatCo.html',{"form":form,"code":cob.code ,"ed":1 })
    except:
        return redirect("/dash/hello")

@login_required
def giftU(req,person):
    try:

        man = get_object_or_404(Cust,email = person)

        if(req.method == "POST"):

            form = CouponForm(req.POST)

            if(form.is_valid()):

                name =man.name_prefix+ man.first_name + man.last_name
                dis = 100 *float(req.POST.get("discount_value"))
                valid = req.POST.get("valid_to")
                co = req.POST.get("code")


                subject = 'SaleFind store Coupone !'
                message = f"Congratulation {name} you won coupone! \n coupone with %{dis} valid to {valid}\n code : {co}"
                sender = 'SalFind@gmail.com'
                recipient_list = [person]

                send_mail(subject, message, sender, recipient_list,fail_silently=False,)

                form.save()

                return render(req,"succMessege.html")

        else:

            code = generate_unique_coupon_code()

            form = CouponForm()

        return render(req,'generatCo.html',{"form":form,"code":code ,"send":1})

    except:

        code = generate_unique_coupon_code()

        return render(req,'generatCo.html',{"form":form,"code":code , "messege":"feild to send coupone ,something went wrong !","send":1})

@login_required
def Logout_view(request):
    try:
        logout(request)

        return redirect('SalFind')
    except:
        return redirect('/dash/hello')

@login_required
def top(req):
    try:
        if(req.method == "POST"):
            return redirect(f"/dash/manageUser/gifts/Cop/{req.POST.get('num')}")
        else:
            return render(req,"gtop.html" , {"t":1})
    except:
        return redirect("/dash/hello")

@login_required
def Gtop(req,num):

    try:
        if(req.method == "POST"):
        
            form = CouponForm(req.POST)

            if(form.is_valid()):
                top_cust = (
                    Cust.objects.annotate(order_count=Count('order__id'))
                    .values('order_count', 'name_prefix', 'full_name', 'email' )
                    .order_by('-order_count')
                )
        
                top = top_cust[0:num]

                for item in top :

                    name =item["name_prefix"] + item["full_name"]
                    dis = 100 *float(req.POST.get("discount_value"))
                    valid = req.POST.get("valid_to")
                    co = req.POST.get("code")

                    subject = 'SaleFind store Coupone !'
                    message = f"Congratulation {name} you won coupone! \n coupone with %{dis} valid to {valid}\n code : {co}"
                    sender = 'SalFind@gmail.com'
                    recipient_list = [item["email"]]
                    send_mail(subject, message, sender, recipient_list,fail_silently=False,)

                form.save()

                return render(req,"succMessege.html")

        else:

            code = generate_unique_coupon_code()

            form = CouponForm()

        return render(req,"generatCo.html",{"form":form ,"code":code})
    except:
        return redirect("/dash/hello")

@login_required
def lower(req):
    try:
        if(req.method == "POST"):
            return redirect(f"/dash/manageUser/gifts/CopL/{req.POST.get('num')}")
        else:
            return render(req,"gtop.html" )
    except:
        return redirect("/dash/hello")

@login_required
def Ltop(req,num):

    try:
        if(req.method == "POST"):
        
            form = CouponForm(req.POST)

            if(form.is_valid()):
                top_cust = (
                    Cust.objects.annotate(order_count=Count('order__id'))
                    .values('order_count', 'name_prefix', 'full_name', 'email' )
                    .order_by('order_count')
                )
        
                top = top_cust[0:num]

                for item in top :

                    name =item["name_prefix"] + item["full_name"]
                    dis = 100 *float(req.POST.get("discount_value"))
                    valid = req.POST.get("valid_to")
                    co = req.POST.get("code")

                    subject = 'SaleFind store Coupone !'
                    message = f"Congratulation {name} you won coupone! \n coupone with %{dis} valid to {valid}\n code : {co}"
                    sender = 'SalFind@gmail.com'
                    recipient_list = [item["email"]]
                    send_mail(subject, message, sender, recipient_list,fail_silently=False,)

                form.save()

                return render(req,"succMessege.html")

        else:

            code = generate_unique_coupon_code()

            form = CouponForm()

        return render(req,"generatCo.html",{"form":form ,"code":code})
    except:
        return redirect("/dash/hello")
