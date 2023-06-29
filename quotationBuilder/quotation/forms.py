from django import forms
from django.contrib.auth.models import User
# from django import widgets
from .models import *
from django import forms
from .models import QuotationMainRequest, QuotationRoomRequest, Hotel, HotelRate, Company

class UserLoginForm(forms.ModelForm):
    email = forms.CharField(
                            widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
                            required=True)
    password = forms.CharField(
                            widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
                            required=True)

    class Meta:
        model=User
        fields=['username','password']


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'address_line1', 'area', 'country', 'hotel_description',
                  'bedroom_pic', 'diningroom_pic', 'receptionroom_pic', 'description_first_day',
                  'description_full_day', 'description_last_day', 'hotel_logo']

class HotelUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'address_line1', 'area', 'country', 'hotel_description',
                  'bedroom_pic', 'diningroom_pic', 'receptionroom_pic', 'description_first_day',
                  'description_full_day', 'description_last_day', 'hotel_logo']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_description']

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_description']


class HotelRateForm(forms.ModelForm):
    class Meta:
        model = HotelRate
        fields = ['hotel_name', 'rate_type', 'rate_season', 'package_type', 'room_type',
                  'room_category', 'traveller_type', 'rate_currency', 'adult_rate', 'child_rate',
                  'young_child_sharing_rate', 'old_child_sharing_rate', 'date_applicable_from',
                  'date_applicable_to', 'company_applicable_to']
        
class HotelRateUpdateForm(forms.ModelForm):
    class Meta:
        model = HotelRate
        fields = ['hotel_name', 'rate_type', 'rate_season', 'package_type', 'room_type',
                  'room_category', 'traveller_type', 'rate_currency', 'adult_rate', 'child_rate',
                  'young_child_sharing_rate', 'old_child_sharing_rate', 'date_applicable_from',
                  'date_applicable_to', 'company_applicable_to']
        
## THESE COULD BE USED WITH POSTGRESSQL
class QuotationMainRequestForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Hotel.objects.values_list('country', flat=True).distinct())
    area = forms.ModelChoiceField(queryset=Hotel.objects.values_list('area', flat=True).distinct())
    hotel_name = forms.ModelChoiceField(queryset=Hotel.objects.values_list('hotel_name', flat=True).distinct())
    
    # country = forms.ModelChoiceField(queryset=Hotel.objects.distinct('country').values_list('country', 'country'))
    # area = forms.ModelChoiceField(queryset=Hotel.objects.distinct('area').values_list('area', 'area'))
    # hotel_name = forms.ModelChoiceField(queryset=Hotel.objects.values_list('hotel_name', 'hotel_name'))

    class Meta:
        model = QuotationMainRequest
        fields = ['date_from', 'date_to',   'country', 'area', 
                  'hotel_name', 
                  'number_adult_resident', 'number_adult_nonresident', 
                  'number_child_resident', 'number_child_nonresident']

class QuotationRoomRequestForm(forms.ModelForm):
    package_type = forms.ModelChoiceField(queryset=HotelRate.objects.values_list('package_type', flat=True).distinct())
    room_category = forms.ModelChoiceField(queryset=HotelRate.objects.values_list('room_category', flat=True).distinct())
    room_type = forms.ModelChoiceField(queryset=HotelRate.objects.values_list('room_type', flat=True).distinct())
    
    # package_type = forms.ModelChoiceField(queryset=HotelRate.objects.distinct('package_type').values_list('package_type', 'package_type'))
    # room_category = forms.ModelChoiceField(queryset=HotelRate.objects.distinct('room_category').values_list('room_category', 'room_category'))
    # room_type = forms.ModelChoiceField(queryset=HotelRate.objects.distinct('room_type').values_list('room_type', 'room_type'))

    class Meta:
        model = QuotationRoomRequest
        fields = ['quotation_id', 'package_type', 'room_category', 'room_type', 'no_of_rooms_for_category_type', 'no_of_adults_sharing', 'no_of_old_children_sharing', 'no_of_young_children_sharing']

QuotationRoomRequestFormSet = forms.inlineformset_factory(
    QuotationMainRequest,
    QuotationRoomRequest,
    form=QuotationRoomRequestForm,
    extra=1,
    can_delete=True
)


# class QuotationMainRequestForm(forms.ModelForm):
#     class Meta:
#         model = QuotationMainRequest
#         fields = ['date_from', 'date_to', 'country', 'area', 'hotel_name', 'number_adult_citizen', 'number_adult_resident', 'number_adult_nonresident', 'number_child_citizen', 'number_child_resident', 'number_child_nonresident']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['country'].queryset = Hotel.objects.values_list('country', flat=True).distinct()
#         self.fields['area'].queryset = Hotel.objects.values_list('area', flat=True).distinct()
#         self.fields['hotel_name'].queryset = Hotel.objects.all()

# class QuotationRoomRequestForm(forms.ModelForm):
#     class Meta:
#         model = QuotationRoomRequest
#         fields = ['quotation_id', 'package_type', 'room_category', 'room_type', 'no_of_rooms_for_category_type', 'no_of_adults_sharing', 'no_of_old_children_sharing', 'no_of_young_children_sharing']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['package_type'].queryset = HotelRate.objects.values_list('package_type', flat=True).distinct()
#         self.fields['room_category'].queryset = HotelRate.objects.values_list('room_category', flat=True).distinct()
#         self.fields['room_type'].queryset = HotelRate.objects.values_list('room_type', flat=True).distinct()


# class QuotationRoomRequestForm(forms.ModelForm):
#     class Meta:
#         model = QuotationRoomRequest
#         fields = '__all__'
#         exclude = ('unique_id',)

# class CreateQuotationForm(forms.ModelForm):
#     class Meta:
#         model = QuotationMainRequest
#         fields = ('date_from', 'date_to', 'country', 'area', 'hotel_name')


 



#     def __init__(self, *args, **kwargs):
#         super(CreateQuotationForm, self).__init__(*args, **kwargs)
        
#         if not hasattr(self, 'cleaned_data'):
#             self.cleaned_data = {}
#         self.fields['country'].choices = self.get_country_choices()
#         self.fields['area'].choices = self.get_area_choices()
#         self.fields['hotel_name'].choices = self.get_hotel_choices()

#     def get_country_choices(self):
#         # Retrieve distinct country values from HotelRate model
#         country_choices = HotelRate.objects.order_by().values_list('hotel_name__country', flat=True).distinct()
#         return [(country, country) for country in country_choices]

#     def get_area_choices(self):
#         # Retrieve distinct area values from HotelRate model based on the selected country
#         country = self.cleaned_data.get('country')
#         area_choices = HotelRate.objects.filter(hotel_name__country=country).order_by().values_list('hotel_name__area', flat=True).distinct()
#         return [(area, area) for area in area_choices]

#     def get_hotel_choices(self):
#         # Retrieve hotel names from HotelRate model based on the selected country and area
#         country = self.cleaned_data.get('country')
#         area = self.cleaned_data.get('area')
#         hotel_choices = HotelRate.objects.filter(hotel_name__country=country, hotel_name__area=area).order_by().values_list('hotel_name__hotel_name', flat=True).distinct()
#         return [(hotel, hotel) for hotel in hotel_choices]
