from rest_framework.pagination import PageNumberPagination

class ParkingListPagination(PageNumberPagination):
    page_size=10