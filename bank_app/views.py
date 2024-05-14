from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import os
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail

# Create your views here.


def index(request):
    return render(request, "index.html")


def Login(request):
    if request.method == "POST":
        a = Logform(request.POST)
        if a.is_valid():
            un = a.cleaned_data['uname']
            p = a.cleaned_data['pin']
            b = Regmodel.objects.all()
            for i in b:
                if i.uname == un and i.pin == p:
                    request.session['id'] = i.id
                    return redirect(profile)
            else:
                return HttpResponse("Login failed")
    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        a = Regform(request.POST, request.FILES)
        if a.is_valid():
            fn = a.cleaned_data['fname']
            ln = a.cleaned_data['lname']
            un = a.cleaned_data['uname']
            em = a.cleaned_data['email']
            ph = a.cleaned_data['phone']
            ac = int("15" + str(ph))
            im = a.cleaned_data['img']
            p = a.cleaned_data['pin']
            rp = a.cleaned_data['rpin']
            if p == rp:
                b = Regmodel(fname=fn, lname=ln, uname=un, email=em, phone=ph, img=im, pin=p, balance=0, ac_num=ac)
                b.save()
                subject = "Your account has been created"
                message = f"Your new account number is {ac}"
                email_from = "bankprj95@gmail.com"
                email_to = em
                send_mail(subject, message, email_from, [email_to])
                return redirect(Login)
            else:
                return HttpResponse("Pin doesn't match")
        else:
            return HttpResponse("Registration failed")
    return render(request, "reg.html")


def profile(request):
    try:
        id1 = request.session['id']
        a = Regmodel.objects.get(id=id1)
        img = str(a.img).split('/')[-1]
        return render(request, "profile.html", {'a': a, 'img': img})
    except:
        return redirect(Login)


def editpro(request, id):
    a=Regmodel.objects.get(id=id)
    if request.method == 'POST':
        a.fname = request.POST.get('fname')
        a.lname = request.POST.get('lname')
        a.email = request.POST.get('email')
        a.phone = request.POST.get('phone')
        a.save()
        return redirect(profile)
    return render(request, 'editpro.html', {'a': a})


def editpic(request, id):
    a = Regmodel.objects.get(id=id)
    img = str(a.img).split('/')[-1]
    if request.method == 'POST':
        a.uname = request.POST.get('uname')
        if len(request.FILES) != 0:
            if len(a.img) != 0:
                os.remove(a.img.path)
            a.img = request.FILES['img']
        a.save()
        return redirect(profile)
    return render(request, 'editpic.html', {'a': a, 'img': img})


# deposit function
def amountadd(request, id):
    x = Regmodel.objects.get(id=id)
    if request.method == "POST":
        am = request.POST.get('amount')
        request.session['amount'] = am
        request.session['ac_num'] = x.ac_num
        x.balance += int(am)
        x.save()
        b = depositamount(amount=am, uid=request.session['id'])
        b.save()
        pin = request.POST.get('pin')
        if int(pin) == x.pin:
            return redirect(credited)
        else:
            return HttpResponse("amount added failed")
    return render(request, "addamount.html")


def credited(request):
    amount = request.session['amount']
    acc = request.session['ac_num']
    return render(request, 'credited.html', {'a': amount, 'ac': acc})


def withdraw(request, id):
    x = Regmodel.objects.get(id=id)
    if request.method == "POST":
        am = request.POST.get('amount')
        request.session['amount'] = am
        request.session['ac_num'] = x.ac_num
        if x.balance >= int(am):
            x.balance -= int(am)
            x.save()
            b = withdrawamount(amount=am, uid=request.session['id'])
            b.save()
            pin = request.POST.get('pin')
            if int(pin) == x.pin:
                return redirect(debited)
            else:
                return HttpResponse("withdrawal failed")
    return render(request, "withdraw.html")


def debited(request):
    amount = request.session['amount']
    ac = request.session['ac_num']
    return render(request, "debited.html", {'am': amount, 'acc': ac})


def check(request):
    id1 = request.session['id']
    a = Regmodel.objects.get(id=id1)
    if request.method == 'POST':
        request.session['ac_num'] = a.ac_num
        request.session['balance'] = a.balance
        pin = request.POST.get('pin')
        if int(pin) == a.pin:
            return redirect(show)
        else:
            return HttpResponse("invalid pin")
    return render(request, 'checkbalance.html')


def show(request):
    acc = request.session['ac_num']
    bal = request.session['balance']
    return render(request, "showbalance.html", {'bal': bal, 'acc': acc})


def ministatement(request, id):
    data = Regmodel.objects.get(id=id)
    pin = request.POST.get('pin')
    if request.method == 'POST':
        if int(pin) == data.pin:
            a = request.POST.get('choice')
            if a == 'deposit':
                return redirect(depositmini)
            elif a == 'withdraw':
                return redirect(withdrawmini)
        else:
            return HttpResponse("invalid password")
    return render(request, "ministatement.html")


def depositmini(request):
    mt = depositamount.objects.all() #fetchall
    id = request.session['id']
    return render(request, 'showdeposit.html', {'mt': mt, 'id': id})


def withdrawmini(request):
    mt = withdrawamount.objects.all()
    id = request.session['id']
    return render(request, "showwithdraw.html", {'mt': mt, 'id': id})


def logout_view(request):
    logout(request)
    return redirect(Login)


def adminlogin(request):
    if request.method == "POST":
        a = adminform(request.POST)
        if a.is_valid():
            us = a.cleaned_data['username']
            ps = a.cleaned_data['password']
            user = authenticate(request, username=us, password=ps)
            if user is not None:
                return redirect(adminindex)
            else:
                return HttpResponse("Login failed")
    return render(request, "adminlog.html")


def adminindex(request):
    return render(request, 'adminindex.html')


def news(request):
    if request.method == 'POST':
        a = newsform(request.POST)
        if a.is_valid():
            tp = a.cleaned_data['topic']
            cn = a.cleaned_data['content']
            b = newsfeed(topic=tp, content=cn)
            b.save()
            return redirect(adminindex)
        else:
            return HttpResponse("failed")
    return render(request, 'news.html')


def newsdisplay(request):
    a = newsfeed.objects.all()
    return render(request, 'newsdisplay.html', {'p': a})


# admin news display
def adminnews(request):
    a = newsfeed.objects.all()
    return render(request, 'adminnews.html', {'p': a})


def newsedit(request, id):
    a = newsfeed.objects.get(id=id)
    if request.method == 'POST':
        a.topic = request.POST.get('topic')
        a.content = request.POST.get('content')
        a.save()
        return redirect(adminnews)
    return render(request, "newsedit.html", {'a': a})


def newsdelete(request, id):
    a = newsfeed.objects.get(id=id)
    a.delete()
    return redirect(adminnews)


def savednews(request, id):
    a = newsfeed.objects.get(id=id)
    s = savenew.objects.all()
    for i in s:
        if i.newsid == a.id and i.uid == request.session['id']:
            return HttpResponse("Already saved")
    b = savenew(topic=a.topic, content=a.content, date=a.date, newsid=a.id, uid=request.session['id'])
    b.save()
    return HttpResponse("News saved")


def showsavednews(request):
    a = newsfeed.objects.all()
    id1 = request.session['id']
    return render(request, "showsavednews.html", {'a': a, 'id': id1})


def forgot_password(request):
    a = Regmodel.objects.all()
    if request.method == 'POST':
        em = request.POST.get('email')
        ac = request.POST.get('account_no')
        for i in a:
            if i.email == em and i.ac_num == int(ac):
                id = i.id
                subject = "Password reset"
                message = f"http://127.0.0.1:8000/bank_app/change_password/{id}"
                email_from = "bankprj95@gmail.com"
                email_to = em
                send_mail(subject, message, email_from, [email_to])
                return redirect(reset_password)
        else:
            return HttpResponse("Oops somthing went wrong !")
    return render(request, "forgot_password.html")


def reset_password(request):
    return render(request, "reset_password.html")


def change_password(request, id):
    a = Regmodel.objects.get(id=id)
    if request.method == "POST":
        p1 = request.POST.get('pin')
        p2 = request.POST.get('rpin')
        if p1 == p2:
            a.pin = p1
            a.save()
            return HttpResponse("Password changed")
        else:
            return HttpResponse("Sorry something went wrong !")
    return render(request, "change_password.html")

