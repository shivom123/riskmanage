from django.conf.urls import url, include
from .import views 

app_name = "RiskApp"

urlpatterns = [
    url(r'^$', views.landingPage, name='home'),
    url(r'models/', views.ManageModel, name='manage_model'),
    url(r'risk/', views.all_risks, name='risk_template'),
    url(r'single_types/', views.single_type, name='single_risk'),
]