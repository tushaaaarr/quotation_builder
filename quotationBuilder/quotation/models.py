from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4  
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from quotationBuilder.custom.mixins_models import  TimeStampMixin


class UserType(models.Model):
    is_hotel_staff = models.BooleanField(default=False)
    is_company_staff = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        if self.is_company_staff == True:
            return "Company staff--" + str(' ') +  str(self.user)
        elif self.is_hotel_staff == True:
            return "Hotel staff--" + str(' ') + str(self.user)



# Create your models here.

class Employee(TimeStampMixin):
    username = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    hotel_staff = models.BooleanField(default=False)
    company_staff = models.BooleanField(default=False)

    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')

 # utility fields
    employee_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)

    def __str__(self) -> str:
        string = f"{self.username}, Hotel Staff: {self.hotel_staff}, Company Staff: {self.company_staff}"
        return string
    
    def clean(self):
        if self.hotel_staff and self.company_staff:
            raise ValidationError("An employee cannot be both hotel staff and company staff.")
        
        if (not self.hotel_staff) and (not self.company_staff):
            raise ValidationError("An employee must be either hotel staff or company staff.")
        
    def save(self, *args, **kwargs):
        string = f"{self.username}, Hotel Staff: {self.hotel_staff}, Company Staff: {self.company_staff}"

        if self.employee_id is None:
            self.employee_id = str(uuid4()).split('-')[4]
            self.slug = slugify(string)

        self.slug = slugify(string)

        super(Employee, self).save(*args, **kwargs)


class Company(TimeStampMixin):

    # Basic Fields
    company_name = models.CharField(null=True, blank=True, max_length=200)
    company_description = models.CharField(null=True, blank=True, max_length=200)
    company_logo = models.ImageField(default='default_logo.jpg', upload_to='Company_logo')
    company_logo_watermark = models.ImageField(default='default_logo.jpg', upload_to='Company_logo')
    company_header = models.ImageField(default='default_logo.jpg', upload_to='Company_header')
    company_footer = models.ImageField(default='default_logo.jpg', upload_to='Company_footer')

    # utility fields
    company_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)

    def __str__(self) -> str:
        string = f"{self.company_name} {self.company_id}"
        return string   

    def save(self, *args, **kwargs):
        string = f"{self.company_name} {self.company_id}"

        if self.company_id is None:
            self.company_id = str(uuid4()).split('-')[4]
            self.slug = slugify(string)

        self.slug = slugify(string)

        super(Company, self).save(*args, **kwargs)


class Hotel(TimeStampMixin):

    # Basic Fields
    hotel_name = models.CharField(null=True, blank=True, max_length=100)

    address_line1 = models.CharField(null=True, blank=True, max_length=100)
    area = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
 
    hotel_description = models.CharField(null=True, blank=True, max_length=1000)

    bedroom_pic = models.ImageField(default='default_logo.jpg', upload_to='hotel_pics')
    diningroom_pic = models.ImageField(default='default_logo.jpg', upload_to='hotel_pics')
    receptionroom_pic = models.ImageField(default='default_logo.jpg', upload_to='hotel_pics')

    description_first_day = models.CharField(null=True, blank=True, max_length=1000)
    description_full_day = models.CharField(null=True, blank=True, max_length=1000)
    description_last_day = models.CharField(null=True, blank=True, max_length=1000)

    hotel_logo = models.ImageField(default='default_logo.jpg', upload_to='hotel_logos')

    # utility fields
    hotel_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)

    def __str__(self) -> str:
        string = f"{self.hotel_name} {self.hotel_id}"
        return string

    def save(self, *args, **kwargs):
        string = f"{self.hotel_name} {self.hotel_id}"

        if self.hotel_id is None:
            self.hotel_id = str(uuid4()).split('-')[4]
            self.slug = slugify(string)

        self.slug = slugify(string)

        super(Hotel, self).save(*args, **kwargs)


class HotelRate(TimeStampMixin):

    RATESEASON = [('High', 'High'), ('Low', 'Low'), ('Medium', 'Medium'),
                  ('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')
                  ]   
    ROOMCATEGORY = [('Standard', 'Standard'), ('Deluxe', 'Deluxe'), ('Superior', 'Superior')]
    ROOMTYPES = [('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')]

    PACKAGETYPE = [('FB Accomodation Only', 'FB Accomodation Only'), ('All inc', 'all inclusive'),
                   ('Ground', 'Ground'), ('Air', 'Air'), 
                   ('Half Board', 'Half Board'),('Bed & Breakfast', 'Bed & Breakfast')]
    
    TRAVELLERTYPE = [('Resident', 'Resident'), ('Non-Resident', 'Non-Resident')]
    rateCURRENCY = [('KES', 'KES'), ('USD', 'USD')]

    # Basic Fields
    hotel_name = models.ForeignKey(Hotel, on_delete=models.PROTECT)

    rate_type = models.CharField(null=True, blank=True, max_length=200)
    rate_season = models.CharField(choices=RATESEASON, blank=True, max_length=200)

    package_type = models.CharField(choices=PACKAGETYPE, blank=True, max_length=200)
    
    room_type = models.CharField(choices=ROOMTYPES, blank=True, max_length=200)
    
    room_category = models.CharField(choices=ROOMCATEGORY, blank=True, max_length=200)
    traveller_type = models.CharField(choices=TRAVELLERTYPE, blank=True, max_length=200)
    rate_currency = models.CharField(choices=rateCURRENCY, blank=True, max_length=200)

    adult_rate = models.FloatField(null=True, blank=True, help_text="Rate for Adult only sharing (or Single, if RoomType = single)")
    child_rate = models.FloatField(null=True, blank=True, help_text="Rate for child only sharing (or Single, if RoomType = single)")
    young_child_sharing_rate = models.FloatField(null=True, blank=True)
    old_child_sharing_rate = models.FloatField(null=True, blank=True)

    date_applicable_from = models.DateField(null=True, blank=True, max_length=200)
    date_applicable_to = models.DateField(null=True, blank=True, max_length=200)

    company_applicable_to = models.ManyToManyField(Company)

    # utility fields
    unique_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)
    reference = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self) -> str:
        string = f"{self.hotel_name} {self.rate_type} {self.rate_season} {self.room_category} {self.traveller_type} {self.date_applicable_from} {self.date_applicable_to} {self.unique_id}"
        return string
    
    def save(self, *args, **kwargs):
        string = f"{self.hotel_name} {self.rate_type} {self.rate_season} {self.room_category} {self.traveller_type} {self.date_applicable_from} {self.date_applicable_to} {self.unique_id}"

        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify(string)

        self.slug = slugify(string)

        super(HotelRate, self).save(*args, **kwargs)


class QuotationMainRequest(TimeStampMixin):

    # Countries = [('Kenya', 'Kenya')]
    # Area = [('Samburu', 'Samburu'), ('Mara', 'Mara'), ('L. Nakuru', 'L. Nakuru')]
    # TravellerType = [('Citizen', 'Citizen'), ('Resident', 'Resident'), ('Non-Resident', 'Non-Resident')]
    # Hotels = [('Kenya', 'Kenya')]

    Age = [('Under 5', 'Under 5'), ('5-12 years', '5-12 years'), ('Over 12', 'Over 12')]

    # Basic Fields
    date_from = models.DateField(null=True, blank=True, max_length=200)
    date_to = models.DateField(null=True, blank=True, max_length=200)

    country = models.CharField(max_length=255)
    area = models.CharField(max_length=255)

    # TODO: Limit these to all countrys in Hotel.Country
    # country = models.CharField(choices=Countries, blank=True, max_length=200)
    # country = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name='main_request_country')

    # TODO: Limit these to all Area in Hotel.Country
    # area = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name='main_request_area')

    hotel_name = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name='main_request_hotel')

    # traveller type # adult
    number_adult_resident = models.IntegerField(null=True, blank=True, default=0)
    number_adult_nonresident = models.IntegerField(null=True, blank=True, default=0)

    # traveller type # child
    number_child_resident = models.IntegerField(null=True, blank=False, default=0)
    number_child_nonresident = models.IntegerField(null=True, blank=False, default=0)


    # utility fields
    quotation_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)
   
    def __str__(self) -> str:
        string = f"{self.hotel_name} {self.quotation_id}"
        return string
    
    def save(self, *args, **kwargs):
        string = f"{self.hotel_name} {self.quotation_id}"

        if self.quotation_id is None:
            self.quotation_id = str(uuid4()).split('-')[4]
            self.slug = slugify(string)

        self.slug = slugify(string)

        super(QuotationMainRequest, self).save(*args, **kwargs)


class QuotationRoomRequest(models.Model):
    PACKAGETYPE = [('FB Accomodation Only', 'FB Accomodation Only'), ('All inc', 'all inclusive'),
                   ('Ground', 'Ground'), ('Air', 'Air'), 
                   ('Half Board', 'Half Board'),('Bed & Breakfast', 'Bed & Breakfast')]
    
    quotation_id = models.ForeignKey(QuotationMainRequest, on_delete=models.PROTECT)
    # package_type = models.ForeignKey(HotelRate, on_delete=models.PROTECT, related_name='package_type_requests')
    package_type = models.CharField(choices=PACKAGETYPE, blank=True, max_length=200)
   
   
    # room_category = models.ForeignKey(HotelRate, on_delete=models.PROTECT, related_name='room_category_requests')
    # room_type = models.ForeignKey(HotelRate, on_delete=models.PROTECT, related_name='room_type_requests')
    
    no_of_rooms_for_category_type = models.IntegerField(null=True, blank=False, default=1)
    # no_of_adults_single = models.IntegerField(null=True, blank=False, default=1)
    no_of_adults_sharing = models.IntegerField(null=True, blank=False, default=1)
    no_of_children_sharing = models.IntegerField(null=True, blank=False, default=1)
    no_of_old_children_sharing = models.IntegerField(null=True, blank=False, default=0)
    no_of_young_children_sharing = models.IntegerField(null=True, blank=False, default=0)

    # utility fields
    # unique_id = models.SlugField(null=True, blank=True, max_length=200, unique=True)

    # def __str__(self) -> str:
    #     string = f"{self.no_of_rooms_for_category_type} {self.room_category} {self.room_type} {self.quotation_id}"
    #     return string
    
    # def save(self, *args, **kwargs):
    #     string = f"{self.no_of_rooms_for_category_type} {self.room_category} {self.room_type} {self.quotation_id}"

        # if self.unique_id is None:
        #     self.unique_id = str(uuid4()).split('-')[4]
        #     self.slug = slugify(string)

        # self.slug = slugify(string)
        # self.last_updated = timezone.localtime(timezone.now())

        # super(QuotationRoomRequest, self).save(*args, **kwargs)


