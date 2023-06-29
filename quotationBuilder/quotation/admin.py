from django.contrib import admin
from .models import Employee, HotelRate, Hotel, Company, QuotationMainRequest, QuotationRoomRequest

# Register your models here.
admin.site.register(Employee)
admin.site.register(HotelRate)
admin.site.register(Hotel)
admin.site.register(Company)
admin.site.register(QuotationMainRequest)
admin.site.register(QuotationRoomRequest)

