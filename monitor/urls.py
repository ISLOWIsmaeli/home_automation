from django.urls import path
from . import views


urlpatterns = [
    # path("",views.index ,name="index"),
    path("", views.home, name="home"),
    path("ajax-response",views.display_led_status,name="ajax_response")
]
