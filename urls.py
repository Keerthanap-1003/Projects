from . import views
from django.urls import path
urlpatterns = [
    path('register/',views.RegisterView.as_view(), name="register"),
    path('all_customer_view/',views.AllCustomersView.as_view(), name='all_customer_view'),
    path('list-pending-customer/', views.ListPendingCustomers.as_view(), name='list-pending-customer'),
    path('list-approove-customers/',views.ListApprooveCustomer.as_view(), name='list-approove-customers'),
    path('list_staff/',views.ListStaff.as_view(), name='list_staff'),
    path('list-managers/', views.ListManager.as_view(), name='list-managers'),
    path('approve-customer/<int:customer_id>/',views.ApproveCustomersView.as_view(), name='approve-customer'),
    path('reject-customer/<int:customer_id>/', views.RejectCustomerView.as_view(), name='reject-customer'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('update-user/<int:id>/',views.UpdateUser.as_view(), name='update_user_details'),
    path('profile/',views.UserProfile.as_view(),name='profile'),
   
]