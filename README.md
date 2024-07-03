Banking Applicaton

It has 3 modules:users_management,account_management,transaction_management.
It has 4 users:Admin,Manager,Staff,Customer


Admin create using command:python manage.py createsuperuser with  emailId,firstname,userType,approvalStatus and  password.
Here superuser is used as admin

Sample data:

emailId:admin@gmail.com
password:Admin@2023
firstName:Admin
userType:admin
approvalStatus:approved



1.path('bankapp/register/',views.RegisterView.as_view(), name="register"),

For staff registeration using this fileds:
Sample data:
firstName:Anamika
lastName:K
email:anamika@gmail.com
username:ammu
phoneNumber:8590923292
address:xx
pinCode:673012
dob:2000-10-03
useType:staff
approovalStatus:approved
password:Anamika@2023

For manager registeration using this fileds:
Sample data:

firstName:Keerthana
lastName:K
email:keerthanap@gmail.com
username:keerthana
phoneNumber:9645639929
address:xx
pinCode:673012
dob:2000-10-03
useType:manager
approovalStatus:approved
password:Keerthana@2023

For customer registeration using this fileds:
Sample data:

firstName:Athira
lastName:P
email:athira@gmail.com
username:athira
phoneNumber:9645639929
address:xx
pinCode:673012
dob:2000-10-03
useType:customer
password:Athira@2023

2.path('bankapp/login/', LoginView.as_view(), name='login'),

Sample data:

For admin:
email:admin@gmail.com
password:Admin@2023

For customer:
email:athira@gmail.com
password:Athira@2023

For manager:
email:keerthanap@gmail.com
password:Keerthana@2023

For staff:

email:anamika@gmail.com
password:Anamika@2023



3.path('bankapp/approve-customer/<int:customer_id>/', ApproveCustomersView.as_view()), 

Sample data:
approvalStatus = approoved

4.path('bankapp/reject-customer/<int:customer_id>/', RejectCustomerView.as_view())


Sample data:
approvalStatus = rejected

5.path:('bankapp/all_customer_view/', AllCustomersView, basename='all_customer_view')


6.path('bankapp/list-pending-customer',ListPendingCustomers,basename='list-pending-customer')


7.path:('bankapp/list-approove-customers', ListApprooveCustomers name='list-approove-customers')


8.path('bankapp/list_staff', ListStaff, name='list_staff')


9.path('bankapp/list-managers', ListManager, name='list-managers')

10.path('update-user/<int:id>/',views.UpdateUser.as_view(), name='update_user_details'),

Sampledata

firstName: "Keerthana"


11.path('bankapp/create-account/', CreateAccountView.as_view(), name='create-account'),


Sample data
customerId:3
accountType:savings

12.path('bankapp/account-management',views.AccountView.as_view(),name='account-management'),

13.path('bankapp/close-account/<int:customer_id>/', CloseAccount.as_view(), name='close-account'),

Sample data:
accountStatus=closed

14.path('active-account-view/',views.ActiveAccountView.as_view(),name='active-account-view'),

15.path('customer_account_details/', views.CustomerAccountDetails.as_view(), name='customer_account_details'),

16.path('bankapp/make-transaction/<int:account_id>/', MakeTransactionView, name='make-transaction')

Sample data
transactionType:deposit
amount:100
transactionStatus:success

17.path('bankapp/list-all-transaction', ListAllTransactionView, name='list-all-transaction')

18.path('bankapp/download_all_transaction_details', DownloadAllTransactionDetails, name='download_transaction_details')

19.path('bankapp/customer-transactions/<int:customer_id>/', CustomerTransactionsView.as_view(), name='customer-transactions'),

20.path('customer-transactions-download/<int:customer_id>/',views.CustomerTransactionsDownload.as_view(), name='customer-transactions-download'),
    