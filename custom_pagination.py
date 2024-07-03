from rest_framework.pagination import LimitOffsetPagination

#Define custom pagination function 
class CustomPagination(LimitOffsetPagination):
    default_limit=2
    