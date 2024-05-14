from django import forms


class Logform(forms.Form):
    uname = forms.CharField(max_length=50)
    pin = forms.IntegerField()


class Regform(forms.Form):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    uname = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.IntegerField()
    img = forms.FileField()
    pin = forms.IntegerField()
    rpin = forms.IntegerField()


class newsform(forms.Form):
    topic = forms.CharField(max_length=50)
    content = forms.CharField(max_length=500)


class adminform(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20)