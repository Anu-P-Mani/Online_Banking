from django.urls import path
from .views import *


urlpatterns = [
    path("index/", index),
    path("login/", Login),
    path("reg/", register),
    path("profile/", profile),
    path("editprofile/<int:id>", editpro),
    path("editimg/<int:id>", editpic),
    path("amountadd/<int:id>", amountadd),
    path("credited/", credited),
    path("withdraw/<int:id>", withdraw),
    path("debited/", debited),
    path("check/", check),
    path("show/", show),
    path('mini/<int:id>', ministatement),
    path('mini1/', depositmini),
    path("mini2/", withdrawmini),
    path("logout/", logout_view),
    path("adminlog/", adminlogin),
    path('admin/', adminindex),
    path('news/', news),
    path('newsdisplay/', newsdisplay),
    path('adnews/', adminnews),
    path('editnews/<int:id>', newsedit),
    path('newsdel/<int:id>', newsdelete),
    path("saved/<int:id>/", savednews),
    path('savedis/', showsavednews),
    path('forgot/', forgot_password),
    path('reset/', reset_password),
    path('change_password/<int:id>', change_password),

]
