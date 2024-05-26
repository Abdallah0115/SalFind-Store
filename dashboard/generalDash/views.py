from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import searchForm, CustForm, sessForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import guest, sess
from .Analysis import Analysis
import pandas as pd
import random
import string



def Log(req):

    try:
        if req.method == 'POST':

            username = req.POST.get('username')

            password = req.POST.get('password')

            user = authenticate(req, username=username, password=password) 

            cu = guest.objects.get(email = req.POST.get('username'))

            if (user and cu):

                login(req, user)

                return redirect('/generalDash/session')

            else:
                    return render(req, 'cusLogin.html', {'error': 'Invalid username or password'})

        return render(req, 'cusLogin.html')
    except:

        return render(req, 'cusLogin.html', {'error': 'Invalid username or password'})

def Emailenter(req):
    try:

        if(req.method == "POST"):
            if(req.POST.get("Custmail")):

                va = searchForm(req.POST)

                if(va.is_valid() ):
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    hashCode = make_password(code)
                    subject = 'SaleFind store Coupone !'
                    message = f"we gona check that it's yor email the verification code is {code}"
                    sender = 'SalFind@gmail.com'
                    recipient_list = [req.POST.get("Custmail")]
                    send_mail(subject, message, sender, recipient_list,fail_silently=False)
                    req.session["username"] = req.POST.get("Custmail")
                    req.session["code"] = hashCode
                    return redirect("/generalDash/Valid")

                else:

                    return render(req ,"emailValid.html" ,{"Error":"NOT VALID !"})

        else:
            return render(req ,"emailValid.html")
    
        return render(req ,"emailValid.html")
    except:
        return render(req, 'genOops.html')

def validation(req ):
    try:
        if(req.method == "POST"):
        
            if(req.POST.get("CustValid")):
                if(check_password(req.POST.get("CustValid"),req.session.get("code"))):
                    return redirect("/generalDash/sign")
                else:
                    return render(req,"valid.html" ,{"Error":"NOT VALID !"})
        else:
            return render(req,"valid.html" )
    
        return render(req,"valid.html" )
    except:
        return render(req, 'genOops.html')

def Sign(req):

    try:
        if(req.method == "POST"):

            form = CustForm(req.POST , req.FILES)

            if(form.is_valid() ):

                form.save()

                return redirect('/generalDash/login')

        else:

            form = CustForm()

        return render(req,'signGeneral.html',{'form':form , "email":req.session.get("username")})
    except:
        return render(req, 'genOops.html')

@login_required
def Sess(req):

    try:

        us = get_object_or_404(guest,email = req.user.username)

        ob = sess.objects.filter(gues=us)

        return render(req,"sess.html",{"sess":ob})

    except:

        return render(req, 'genOops.html')


def VCsv(df):
    expected_columns = ['order_id', 'order_date', 'status', 'item_id', 'sku', 'qty_ordered',
                        'price', 'value', 'discount_percentage', 'discount_amount', 'total',
                        'category', 'payment_method', 'bi_st', 'cust_id', 'year', 'month',
                        'ref_num', 'Name Prefix', 'First Name', 'Middle Initial', 'Last Name',
                        'Gender', 'age', 'full_name', 'E Mail', 'SSN', 'Phone No. ',
                        'Place Name', 'County', 'City', 'State', 'Zip', 'Region', 'User Name']
    col = df.columns
    for fe in col:
        if(fe not in expected_columns):
            return True
        

    nu = df.isnull().sum()

    for fet in nu:
        if(fet / df.shape[0] >= 0.3):
            return True
    return False

@login_required
def creatSess(req):
    try:

        if(req.method == "POST"):
            mod = req.POST.copy()
            mod["gues"] = guest.objects.get(email = req.user.username)
            req.POST=mod
            se = sessForm(mod,req.FILES)
            file = req.FILES['csv_file']

            if(se.is_valid()):

                df = pd.read_csv(file)

                if(VCsv(df)):

                    return render(req,"createSession.html",{'form':se,'error':"Not Valid data"})

                se.save()

                return redirect('/generalDash/session')

            else:

                return render(req,"createSession.html",{'form':se,'error':"Not valid input"})
        else:
            se = sessForm()
            return render(req,"createSession.html",{'form':se})
    except:
        return render(req, 'genOops.html')

@login_required
def Home(req ,obj ,num):

    try:
        ob = sess.objects.get(id = obj)

        csv_file_path = ob.csv_file.path

        charts = Analysis(csv_file_path)

        if(num == 1):

            user = req.user.username

            total_peices = charts.total_peices()

            total_money = charts.gauge_total()

            chart = charts.total_per_mon()

            total_disc = charts.total_disc()

            total_cust = charts.total_cust()

            return render(req,'home2.html' ,{'user':user ,
                                        'peices':total_peices,
                                        'disc':round(total_disc),
                                        'cust':total_cust,
                                        'money':total_money,
                                        'graph':chart,
                                        'obj':obj})

        elif(num == 2):
            chart = charts.total_Sales_By_Destrib_By_Month()

            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income Per Month",'obj':obj})
    
        elif(num == 3):
            chart = charts.Total_Sales_By_Category()

            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Category",'obj':obj})

        elif(num == 4):

            chart = charts.Total_Sales_By_Gender()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Gender",'obj':obj})
    
        elif(num == 5):

            chart = charts.plot_income_by_age_group()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Age Group",'obj':obj})

        elif(num == 6):

            chart = charts.plot_sales_by_status()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Status",'obj':obj})
    
        elif(num == 7):

            chart = charts.Total_Sales_by_Payment_Method()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Payment Method",'obj':obj})
    
        elif(num == 8):

            chart = charts.Top_10_States_with_Total_Income()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Top 10 States",'obj':obj})
    
        elif(num == 9):

            chart = charts.Low_10_States_with_Total_Income()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Income VS Lowest 10 States",'obj':obj})
    
        elif(num == 10):
            chart = charts.Pie_Chart_of_Status_Distribution()
            canceled = charts.canceld()
            ref = charts.ref()
            char = charts.gauge_order_can()
            return render(req , "incom_per_mon2.html" ,{"graph":chart ,
                                                    "title":"Orders VS Status",
                                                    "mrD":1,
                                                    "gau":char,
                                                    "can":canceled,
                                                    "Ref":ref
                                                    ,'obj':obj})

        elif(num == 11):
            chart = charts.Num_Of_Orders_By_Gendr()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Orders VS Gender",'obj':obj})
    
        elif(num == 12):
            chart = charts.Order_Of_Category()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Orders VS Category",'obj':obj})
    
        elif(num == 13):
            chart = charts.orders_per_state()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Number orders per state",'obj':obj})
    
        elif(num == 14):
            chart = charts.Top_5_Counties_by_Quantity_Ordered()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Top 10 Counties Ordering",'obj':obj})
    
        elif(num == 15):
            chart = charts.Lower_5_Counties_by_Quantity_Ordered()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Lower 10 Counties Ordering",'obj':obj})
    
        elif(num == 16):
            chart = charts.Discount_Percentage_by_Payment_Method()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Discounts VS Payment Method",'obj':obj})
    
        elif(num == 17):
            chart = charts.Average_Discount_Percentage_by_Payment_Method()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Avrage Discounts VS Payment Method",'obj':obj})
    
        elif(num == 18):
            chart = charts.disc_per_month()
            return render(req , "incom_per_mon2.html" ,{"graph":chart , "title":"Discounts VS Date",'obj':obj})

        else:

            user = req.user.username

            total_peices = charts.total_peices()

            total_money = charts.gauge_total()

            chart = charts.total_per_mon()

            total_disc = charts.total_disc()

            total_cust = charts.total_cust()

            return render(req,'home2.html' ,{'user':user ,
                                        'peices':total_peices,
                                        'disc':round(total_disc),
                                        'cust':total_cust,
                                        'money':total_money,
                                        'graph':chart,
                                        'obj':obj})
    except:
        return render(req, 'genOops.html')

@login_required
def Logout_view(req):
    try:
        logout(req)

        return redirect('SalFind')
    except:
        return render(req, 'genOops.html')
