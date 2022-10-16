#from django.conf.urls import url
from django.urls import  re_path
from AssetTransportation import views

urlpatterns =[
    re_path(r'assetAct$',views.assetRequest),
    re_path(r'assetAct/([0-9]+)$',views.assetRequest)]


#from django.urls import include, re_path

#from myapp.views import home

#urlpatterns = [
#    re_path(r'^$', home, name='home'),
#    re_path(r'^myapp/', include('myapp.urls'),
#]
