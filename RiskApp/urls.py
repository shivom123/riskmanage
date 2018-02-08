from django.conf.urls import url, include
from .import views 

app_name = "RiskApp"

urlpatterns = [
    url(r'^$', views.landingPage, name='home'),
    url(r'models/', views.ManageModel, name='manage_model'),
    # url(r'^user_registration/',views.registration, name='registration_temp' ),
    # url(r'^view_pro/',views.view_Profile, name='profile_temp'),
    # url(r'^update_pro/(?P<pk>[0-9]+)$',views.update_profile, name='update_temp' ),
    # url(r'^delete_pro/(?P<pk>[0-9]+)$',views.delete, name="delete_temp"),





]