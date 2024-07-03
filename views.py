from rest_framework import status
from rest_framework import permissions
from  account_management.models import Account

from users_management.models import UserRegistration 
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializer import UserRegisterationSerializer,LoginSerializer,UserUpdateSerializer,ProfileSerializer
from rest_framework.response import Response
from users_management.custom_pagination import CustomPagination
from bank.permissions import ManagerStaff,ManagerAdmin,Admin,Staff,Customer
from django.db.models import Q
from django.contrib.auth.hashers import check_password

#Registeration function to register customers
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        # Use the manager on the UserRegistration model
        if UserRegistration.objects.filter(email=email).exists():
            return Response(
                data={"message": "Email is already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            user.set_password(request.data['password'])
            user.save()
            return Response(
                data={
                    "message": "User Registered successfully"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    

#Serach function to perform,search is used in all listing function.
def search_user_registration(query):
    search_result = UserRegistration.objects.filter(
        Q(firstName__icontains=query) |  
        Q(lastName__icontains=query) |   
        Q(email__icontains=query)|
        Q(phoneNumber__icontains=query)       
    )
    return search_result

#Function to list all customer
class AllCustomersView(APIView):
    permission_classes = [permissions.IsAuthenticated, ManagerStaff]

    def get(self, request):
        query = self.request.GET.get('query')
        if query:
            customers = search_user_registration(query).filter(userType='customer')
        else:
            customers = UserRegistration.objects.filter(userType='customer')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(customers, request)
        serializer = UserRegisterationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
#Function list customer whose staus are pending
class ListPendingCustomers(APIView):
    permission_classes = [permissions.IsAuthenticated, ManagerStaff]
    def get(self, request):
        query = request.GET.get('query')
        if query:
            pending_customers = search_user_registration(query)
        else:
            pending_customers = UserRegistration.objects.filter(userType='customer', approvalStatus='pending')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(pending_customers, request)
        serializer = UserRegisterationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#Function to approove customers
class ListApprooveCustomer(APIView):
    permission_classes = [permissions.IsAuthenticated, ManagerStaff]
    def get(self, request):
        query = request.GET.get('query')
        if query:
             approvedCustomers = search_user_registration(query)
        else:
            approvedCustomers = UserRegistration.objects.filter(userType='customer', approvalStatus='approved')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(approvedCustomers, request)
        serializer = UserRegisterationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


#Function to list staff
class ListStaff(APIView):
    permission_classes = [permissions.IsAuthenticated, ManagerAdmin]

    def get(self, request):
        query = self.request.GET.get('query')
        if query:
            staff = search_user_registration(query).filter(userType='staff')
        else:
            staff = UserRegistration.objects.filter(userType='staff')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(staff, request)
        serializer = UserRegisterationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
#Function to list managers
class ListManager(APIView):
    permission_classes = [permissions.IsAuthenticated,Admin]
    def get(self, request):
        query = request.GET.get('query')
        if query:
            manager = search_user_registration(query).filter(userType='manager')
        else:
            manager = UserRegistration.objects.filter(userType='manager')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(manager, request)
        serializer = UserRegisterationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
# from django.shortcuts import get_object_or_404

# class List(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, id):
#         id=request.user.id
#         manager = get_object_or_404(UserRegistration, id=id)
#         serializer = UserRegisterationSerializer(manager)
#         return Response(serializer.data)
# 


#Function to update user details
class UpdateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, id):
        try:
            user_id = self.kwargs.get('id')
            return UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            return None

    def check_authorization(self, user_type, userType):
        if user_type == 'admin':
            return userType == 'manager'
        elif user_type == 'manager':
            return userType in ['staff','customer']
        elif user_type == 'staff':
            return userType in ['customer']
        return False

    def get(self, request, id=None):
        user = self.get_user(id)
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_type = request.user.userType
        print(user_type)
        print(user.userType)

        if self.check_authorization(user_type, user.userType):
            return Response({
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'phoneNumber': user.phoneNumber,
                'address': user.address,
                'pinCode': user.pinCode
            })
        else:
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id=None):
        user = self.get_user(id)
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_type = request.user.userType
        email = request.data.get('email')
# Exclude the current user's email from the queryset
        if UserRegistration.objects.filter(email=email).exclude(id=user.id).exists():
            return Response(
                data={"message": "Email is already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )


        if user.approvalStatus != 'approved':
            return Response({'message': 'User approval status is not approved. Cannot update details.'}, status=status.HTTP_400_BAD_REQUEST)

        if self.check_authorization(user_type, user.userType):
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User details updated successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


        
#Function to perform login ,login is common for all users      
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serialized_data = LoginSerializer(data=request.data)

        if not serialized_data.is_valid():
            return Response({
                "error": "Invalid input data",
                "errors": serialized_data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serialized_data.validated_data['email']
        password = serialized_data.validated_data['password']

        try:
            user = UserRegistration.objects.get(email=email)
        except UserRegistration.DoesNotExist:
            return Response({
                "error": "User with this email does not exist"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if user.approvalStatus != 'approved':
            return Response({
                "error": "User is not approved"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            refresh = RefreshToken.for_user(user)

            account_id = ''

            try:
                account = user.account.get()
                account_id = account.id
            except Account.DoesNotExist:
                pass

            return Response({
                "message": "Login Success",
                "refreshToken": str(refresh),
                "accessToken": str(refresh.access_token),
                "userType": user.userType,
                "name" : user.firstName,
                "id": {"customerId": user.id},
                "accountId": account_id if account_id else '',  
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Incorrect password"
            }, status=status.HTTP_401_UNAUTHORIZED)





#Function to approove customer  registeration,approove function is done by staff
class ApproveCustomersView(APIView):
    permission_classes = [permissions.IsAuthenticated,Staff]
    def post(self, request, customer_id):
        try:
            customer = UserRegistration.objects.get(id=customer_id)
        except UserRegistration.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        if customer.approvalStatus == 'pending':
            customer.approvalStatus = 'approved'
            customer.save()
            return Response({'message': 'Customer approved successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Customer status is not pending'}, status=status.HTTP_400_BAD_REQUEST)

#Function to reject customers registeration,reject customers is done by staff     
class RejectCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated,Staff]
    def post(self, request, customer_id):
        try:
            customer = UserRegistration.objects.get(id=customer_id)
        except UserRegistration.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        if customer.approvalStatus == 'pending':
            customer.approvalStatus = 'rejected'
            customer.save()
            return Response({'message': 'Customer rejected successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Customer status is not pending '}, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user  
        if user.is_authenticated:
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'User not authenticated'}, status=401)