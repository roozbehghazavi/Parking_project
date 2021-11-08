from rest_framework.pagination import PageNumberPagination

class CarOwnerPagination(PageNumberPagination):
    page_size = 6
