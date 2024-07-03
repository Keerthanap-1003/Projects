from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import UserRegistration
from .serializer import LoginSerializer
from .views import RegisterView
from rest_framework.test import force_authenticate
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "user@gmail.com",
            "password": "Password@123"
        }
        self.user = UserRegistration.objects.create(
            email="user@gmail.com",
            password=make_password("Password@123"),
            approvalStatus="approved"
        )

    def test_valid_login(self):
        url = reverse('login')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_invalid_email(self):
        invalid_data = {
            "email": "notuser@gmail.com",
            "password": "Password@123"
        }
        url = reverse('login')
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
    def test_unapproved_user(self):
        unapproved_user = UserRegistration.objects.create(
            email="notuser@gmail.com",
            password=make_password("Password@123"),
            approvalStatus="pending"
        )
        unapproved_data = {
            "email": "notuser@gmail.com",
            "password": "Password@123"
        }
        url = reverse('login')
        response = self.client.post(url, unapproved_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_incorrect_password(self):
        incorrect_password_data = {
            "email": "user@gmail.com",
            "password": "Password123"
        }
        url = reverse('login')
        response = self.client.post(url, incorrect_password_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class RegisterCustomerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_valid_post(self):
        data = {
            "firstName": "Keer",
            "lastName": "P",
            "email": "kee123@gmail.com",
            "username": "kee",
            "phoneNumber": "8590923292",
            "address": "cccc",
            "pinCode": "673012",
            "dob": "2000-10-03",
            "userType": "customer",
            "approvalStatus": "pending",
            "password": "Keerthan@2023" 
        }

        request = self.factory.post("/bankapp/register/", data)
        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_post(self):
        data = {
            "firstName": "1234",
            "lastName": "P",
            "email": "kee123gmail.com",  
            "username": "kee",
            "phoneNumber": "8590923292",
            "address": "cccc",
            "pinCode": "673012",
            "dob": "2000-10-03",
            "userType": "customer",
            "approvalStatus": "pending",
            "password": "Keerthan@2023" 
        }

        request = self.factory.post("/bankapp/register/", data)
        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AllCustomersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = UserRegistration.objects.create(
            email="staff@gmail.com",
            password=make_password("Password@2023"),
            userType="staff"
        )
        self.customer1 = UserRegistration.objects.create(
            email="customer1@gmail.com",
            userType="customer"
        )
        self.customer2 = UserRegistration.objects.create(
            email="customer2@gmail.com",
            userType="customer"
        )

    def test_valid_list_customers(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('all_customer_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_customers(self):
        url = reverse('all_customer_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class ListPendingCustomersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = UserRegistration.objects.create(
            email="staff@gmail.com.com",
            password=make_password("Password@2023"),
            userType="staff",
            approvalStatus="approved"  
        )
        self.pending_customer1 = UserRegistration.objects.create(
            email="customer1@gmail.com",
            password=make_password("Password@123"),
            userType="customer",
            approvalStatus="pending"
        )
        self.pending_customer2 = UserRegistration.objects.create(
            email="Customer2@gmail.com",
            password=make_password("Password@23"),
            userType="customer",
            approvalStatus="pending"
        )

    def test_list_pending_customers(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('list-pending-customer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_pending_customers_(self):
        url = reverse('list-pending-customer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ApproveCustomersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = UserRegistration.objects.create(
            email="staff@gmail.com",
            password=make_password("Password@2023"),
            userType="staff",
            approvalStatus="approved"  
        )
        self.approve_customer1 = UserRegistration.objects.create(
            email="customer1@gmail.com",
            password=make_password("Password@123"),
            userType="customer",
            approvalStatus="approved"
        )
        self.approve_customer2 = UserRegistration.objects.create(
            email="customer2@gmail.com",
            password=make_password("Password@23"),
            userType="customer",
            approvalStatus="approved"
        )

    def test_list_approve_customers(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('list-approove-customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_approve_customers(self):
        url = reverse('list-approove-customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ListStaffTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager_user = UserRegistration.objects.create(
            email="manager@gmail.com",
            password=make_password("Password@2023"),
            userType="manager",
            approvalStatus="approved"  
        )
        self.approve_staff1 = UserRegistration.objects.create(
            email="staff1@gmail.com",
            password=make_password("Password@123"),
            userType="staff",
            approvalStatus="approved"
        )
        self.approve_staff2 = UserRegistration.objects.create(
            email="staff2@gmail.com",
            password=make_password("Password@23"),
            userType="staff",
            approvalStatus="approved"
        )

    def test_list_valid_staff(self):
        self.client.force_authenticate(user=self.manager_user)
        url = reverse('list_staff')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_staff(self):
        url = reverse('list_staff')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListManagerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = UserRegistration.objects.create(
            email="admin@gmail.com",
            password="Admin@2023",
            firstName="Admin",
            userType="admin",
            approvalStatus="approved"
        )
       
        self.manager = UserRegistration.objects.create(
            email="manager@gmail.com",
            password="Password@2023",
            firstName="Manager",
            userType="manager",
            approvalStatus="approved"
        )

    def test_valid_list_managers(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('list-managers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_managers(self):
        url = reverse('list-managers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class ApproveCustomersViewTestCase(APITestCase):
    def setUp(self):
        self.staff_user = UserRegistration.objects.create_user(
            email='staff@gmail.com',
            password='Password@2023'
            )
        self.staff_user.userType = 'staff'
        self.staff_user.save()

    def test_valid_approve_customer(self):
        self.client.force_authenticate(user=self.staff_user)
        customer = UserRegistration.objects.create(email='customer@gmail.com', approvalStatus='pending')
        url = reverse('approve-customer',args=[customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.approvalStatus, 'approved')

    def test_approve_customer_not_pending(self):
        self.client.force_authenticate(user=self.staff_user)
        customer = UserRegistration.objects.create(username='customer', approvalStatus='approved')
        url = reverse('approve-customer',args=[customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        customer.refresh_from_db()
        self.assertEqual(customer.approvalStatus, 'approved')


class RejectCustomersViewTestCase(APITestCase):
    def setUp(self):
        self.staff_user = UserRegistration.objects.create_user(
            email='staff@gmail.com',
            password='Password@2023'
            )
        self.staff_user.userType = 'staff'
        self.staff_user.save()

    def test_valid_reject_customer(self):
        self.client.force_authenticate(user=self.staff_user)
        customer = UserRegistration.objects.create(email='customer@gmail.com', approvalStatus='pending')
        url = reverse('reject-customer',args=[customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.approvalStatus, 'rejected')

    def test_approve_customer_not_pending(self):
        self.client.force_authenticate(user=self.staff_user)
        customer = UserRegistration.objects.create(username='customer', approvalStatus='rejected')
        url = reverse('reject-customer',args=[customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        customer.refresh_from_db()
        self.assertEqual(customer.approvalStatus, 'rejected')


class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserRegistration.objects.create(
            email='admin@gmail.com',
            userType='admin',
            password=make_password("Password@2023"),
            approvalStatus='approved'
        )
        self.manager_user = UserRegistration.objects.create(
            email='manager@gmail.com',
            userType='manager',
            password=make_password("Password@2023"),
            approvalStatus='approved'
        )
        self.staff_user = UserRegistration.objects.create(
            email='staff@gmail.com',
            userType='staff',
            password=make_password("Password@2023"),
            approvalStatus='approved'
        )
        self.customer_user = UserRegistration.objects.create(
            email='customer@gmail.com',
            userType='customer',
            password=make_password("Password@2023"),
            approvalStatus='approved'
        )

    def test_admin_update_manager_details(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.manager_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_update_staff_details(self):
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.staff_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_update_customer_details(self):
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.customer_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_staff_details(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.staff_user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_update_manager_details(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.manager_user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_update_manager_details(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.manager_user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unapproved_user_update(self):
        self.manager_user.approvalStatus = 'pending'
        self.manager_user.save()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(reverse('update_user_details', kwargs={'id': self.manager_user.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
