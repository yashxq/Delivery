#from django.conf.urls import url
from django.urls import  re_path
from letsride import views

urlpatterns =[
    re_path(r'riderInfo',views.riderInfo),
    re_path(r'createOrder',views.createOrder),
    re_path(r'createRiderTravel',views.createRiderTravel),
    re_path(r'getRequestHistory',views.getRequestHistory),
    re_path(r'getMatchedDeliveryOptions',views.getMatchedDeliveryOptions),
    re_path(r'assignRiderToOrder',views.assignRiderToOrder)

]

#from django.urls import include, re_path

#from myapp.views import home

#urlpatterns = [
#    re_path(r'^$', home, name='home'),
#    re_path(r'^myapp/', include('myapp.urls'),
#]
