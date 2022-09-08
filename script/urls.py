from django.urls import path
from .views import MailView, MailSuccessView

app_name = 'script'
urlpatterns = [

    path('', MailView.as_view(), name='mailview'),
    path('success/', MailSuccessView.as_view(), name="success"),

]
