from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.AccountRegister.as_view(), name='register'),
    path('login/', views.AccountLogin.as_view(), name='login'),
    path('logout/', views.AccountLogout.as_view(), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.AccountActivate.as_view(), name='activate'),
    path('password_reset/', views.UserPassReset.as_view(), name='pwdreset'),
    path('password_reset_done/', views.UserPassResetDone.as_view(),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', views.UserPassResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', views.UserPassResetComplete.as_view(),
         name='password_reset_complete'),
    # User dashboard
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name='account/dashboard/delete_confirm.html'),
         name='delete_confirmation'),

    # Address
    path('addresses/', views.ViewAddress.as_view(), name='addresses'),
    path('add_address/', views.AddAddress.as_view(), name='add_address'),
    path('addresses/edit/<slug:id>/', views.EditeAddress.as_view(), name='edit_address'),
    path('addresses/delete/<slug:id>/', views.DeleteAddress.as_view(), name='delete_address'),
    path('addresses/set_default/<slug:id>/', views.SetDefaultAddress.as_view(), name='set_default_address'),
]
