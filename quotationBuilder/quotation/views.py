from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from quotationBuilder.custom.mixins_views import StatusFieldMixin
from .forms import *
from .models import *
from django.forms import modelformset_factory


from django.contrib.auth.models import User, auth
from random import randint
from uuid import uuid4

from rest_framework import viewsets
import quotation.serializers as serializers_quotation
import quotation.models as models_quotation


from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Create your views here.
@login_required
def dashboard(request):
    context = {}
    return render(request, 'quotation/dashboard.html', context)


# Anonymous required
def anonymous_required(function=None, redirect_url=None):

    if not redirect_url:
        redirect_url = 'dashboard'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def home(request):
    return render(request, 'quotation/index.html')


@anonymous_required
def login(request):
    context = {}
    if request.method == 'GET':
        form = UserLoginForm()
        context['form'] = form
        return render(request, 'quotation/login.html', context)
        # return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)
        if username is not None:
            auth.login(request, user)

            return redirect('dashboard')
        else:
            context['form'] = form
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'quotation/login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
    


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a view that lists all hotels
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'quotation/add_hotel.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def update_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelUpdateForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            # Redirect to a view that shows hotel details
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = HotelUpdateForm(instance=hotel)
    return render(request, 'quotation/update_hotel.html', {'form': form, 'hotel': hotel})


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'quotation/hotel_list.html', {'hotels': hotels})


@login_required
@user_passes_test(lambda u: u.employee.company_staff == True, login_url='login')
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a view that lists all companies
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'quotation/add_company.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.employee.company_staff == True, login_url='login')
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'quotation/company_list.html', {'companies': companies})


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def add_hotel_rate(request):
    if request.method == 'POST':
        form = HotelRateForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a view that lists all hotel rates
            return redirect('hotelrate_list')
    else:
        form = HotelRateForm()
    return render(request, 'quotation/add_hotel_rate.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def hotelrate_list(request):
    hotelrates = HotelRate.objects.all()
    return render(request, 'quotation/hotelrate_list.html', {'hotelrates': hotelrates})


@login_required
@user_passes_test(lambda u: u.employee.company_staff == True, login_url='login')
def update_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            # Redirect to a view that shows company details
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyUpdateForm(instance=company)
    return render(request, 'quotation/update_company.html', {'form': form, 'company': company})


@login_required
@user_passes_test(lambda u: u.employee.hotel_staff == True, login_url='login')
def update_hotel_rate(request, pk):
    hotel_rate = get_object_or_404(HotelRate, pk=pk)
    if request.method == 'POST':
        form = HotelRateUpdateForm(request.POST, instance=hotel_rate)
        if form.is_valid():
            form.save()
            # Redirect to a view that shows hotel rate details
            return redirect('hotel_rate_detail', pk=hotel_rate.pk)
    else:
        form = HotelRateUpdateForm(instance=hotel_rate)
    return render(request, 'quotation/update_hotel_rate.html', {'form': form, 'hotel_rate': hotel_rate})


def create_quatation_new(request):
    hotels = Hotel.objects.all()
    if request.method == "POST":
        country = request.POST.get('country',False)
        area  = request.POST.get('area',False)
        hotel_name  = request.POST.get('hotel_name',False)
        adult_res  = request.POST.get('adult_res',False)
        adult_nonres  = request.POST.get('adult_nonres',False)
        child_res  = request.POST.get('child_res',False)
        child_nonres  = request.POST.get('child_nonres',False)

        # Room request
        package_type = request.POST.get('package_type',False)
        room_category = request.POST.get('room_category',False)
        room_type = request.POST.get('room_type',False)
        no_of_room_category = request.POST.get('no_of_room_category',False)
        no_of_adult_sharing = request.POST.get('no_of_adult_sharing',False)
        old_child_sharing = request.POST.get('old_child_sharing',0)
        yound_child_sharing = request.POST.get('yound_child_sharing',0)

        hotel_instance = Hotel.objects.get(id = hotel_name)
        Quotation_ins = QuotationMainRequest(
            hotel_name = hotel_instance,
            country = country,
            area = area,
            number_adult_resident = adult_res,
            number_adult_nonresident = adult_nonres,
            number_child_resident = child_res,
            number_child_nonresident = child_nonres

        )
        Quotation_ins.save()

        # package_type_q = HotelRate.objects.get(package_type = package_type,hotel_name = hotel_instance)
        HotelRateInstance = HotelRate.objects.filter(hotel_name = hotel_instance)
        HotelRateInstance = HotelRateInstance.filter(
        package_type = package_type,
        room_type = room_type,
        room_category = room_category
        ) 


        QuotationRoomRequest(
            quotation_id = Quotation_ins,
            package_type = HotelRateInstance,
            no_of_rooms_for_category_type = no_of_room_category,
            no_of_adults_sharing = no_of_adult_sharing,
            no_of_children_sharing = float(int(old_child_sharing) + int(yound_child_sharing)),
            no_of_old_children_sharing = old_child_sharing,
            no_of_young_children_sharing = yound_child_sharing
        ).save()

         
        rates = {}
        if adult_nonres:
            if HotelRateInstance.filter(traveller_type = "Non-Resident").exists():
                HotelRateInstance = HotelRateInstance.filter(traveller_type = "Non-Resident")
                rates['adult_nonres'] = HotelRateInstance[0].adult_rate * int(adult_nonres)        

        if child_nonres:
            if HotelRateInstance.filter(traveller_type = "Non-Resident").exists():
                HotelRateInstance = HotelRateInstance.filter(traveller_type = "Non-Resident")
                rates['child_nonres'] = HotelRateInstance[0].child_rate * int(child_nonres)

        if adult_res:
            if HotelRateInstance.filter(traveller_type = "Resident").exists():
                HotelRateInstance = HotelRateInstance.filter(traveller_type = "Resident")
                rates['adult_res'] = HotelRateInstance[0].adult_rate * int(adult_res)

        if child_res:
            if HotelRateInstance.filter(traveller_type = "Resident").exists():
                HotelRateInstance = HotelRateInstance.filter(traveller_type = "Resident")
                rates['child_res'] = HotelRateInstance[0].child_rate * int(child_res)

        print(rates)

        
        print("HotelRateInstance",HotelRateInstance)

    main_form = QuotationMainRequestForm()
    room_formset = QuotationRoomRequestFormSet()

    hotel_dict = {}
    hotel_dict['area']= list(Hotel.objects.values_list('area', flat=True).distinct())
    hotel_dict['country']=list(Hotel.objects.values_list('country', flat=True).distinct())
    
    room_dict = {}
    room_dict['package_type'] = list(HotelRate.objects.values_list('package_type', flat=True).distinct())
    room_dict['room_category'] = list(HotelRate.objects.values_list('room_category', flat=True).distinct())
    room_dict['room_type'] = list(HotelRate.objects.values_list('room_type', flat=True).distinct())

    context = {
        'main_form': main_form,
        'room_formset': room_formset,
        'hotels':hotels,
        "hotel_dict":hotel_dict,
        "room_dict":room_dict
    }


    return render(request,'home/quotation_form.html',context=context)


# THESE COULD BE USED WITH POSTGRESSQL
def create_quotation(request):
    if request.method == 'POST':
        print('we are here.')
        main_form = QuotationMainRequestForm(request.POST)
        room_formset = QuotationRoomRequestFormSet(request.POST)
        if main_form.is_valid() and room_formset.is_valid():
            # Save the main form instance without committing to the database
            # main_instance = main_form.save(commit=False)

            print("main_instance",main_form.cleaned_data)
            print("room_instance",room_formset.cleaned_data)
            
            # Retrieve the hotel instance
            hotel_name = main_form.cleaned_data['hotel_name']
            hotel = get_object_or_404(Hotel, name=hotel_name)

            # Assign the hotel instance to the main instance
            main_instance.hotel_name = hotel

            # Save the main instance to the database
            main_instance.save()

            # Save the room formset instances with the main instance
            for room_form in room_formset:
                room_instance = room_form.save(commit=False)
                room_instance.main_request = main_instance
                room_instance.save()

            # Redirect or perform any other action upon successful form submission
            return HttpResponseRedirect('/success/')
    else:
        main_form = QuotationMainRequestForm()
        room_formset = QuotationRoomRequestFormSet()

   
    context = {
        'main_form': main_form,
        'room_formset': room_formset,
    }

    return render(request, 'quotation/create_quotation_copy.html', context)


# from django.shortcuts import render
# from django.http import JsonResponse
# from .forms import CreateQuotationForm, QuotationRoomRequestForm
# from .models import QuotationMainRequest

# def create_quotation(request):
#     if request.method == 'POST':
#         form = CreateQuotationForm(request.POST)
#         room_request_form = QuotationRoomRequestForm(request.POST, prefix='room')
#         if form.is_valid() and room_request_form.is_valid():
#             quotation = form.save()
#             room_request = room_request_form.save(commit=False)
#             room_request.quotation = quotation
#             room_request.save()
#             return JsonResponse({'success': True})
#         else:
#             errors = {
#                 'form_errors': form.errors,
#                 'room_request_errors': room_request_form.errors,
#             }
#             return JsonResponse({'success': False, 'errors': errors})
#     else:
#         form = CreateQuotationForm()
#         room_request_form = QuotationRoomRequestForm(prefix='room')
#         return render(request, 'quotation/create_quotation.html', {'form': form, 'room_request_form': room_request_form})

# def get_areas(request):
#     country = request.GET.get('country')
#     areas = HotelRate.objects.filter(hotel_name__country=country).order_by().values_list('hotel_name__area', flat=True).distinct()
#     return JsonResponse({'areas': list(areas)})

# def get_hotels(request):
#     country = request.GET.get('country')
#     area = request.GET.get('area')
#     hotels = HotelRate.objects.filter(hotel_name__country=country, hotel_name__area=area).order_by().values_list('hotel_name__hotel_name', flat=True).distinct()
#     return JsonResponse({'hotels': list(hotels)})


# @login_required
# def create_quotation(request):
#     main_form = QuotationMainRequestForm()
#     QuotationRoomRequestFormSet = modelformset_factory(
#         QuotationRoomRequest,
#         form=QuotationRoomRequestForm,
#         extra=1,
#         can_delete=True
#     )
#     room_formset = QuotationRoomRequestFormSet(queryset=QuotationRoomRequest.objects.none())

#     if request.method == 'POST':
#         main_form = QuotationMainRequestForm(request.POST)
#         room_formset = QuotationRoomRequestFormSet(request.POST)

#         if main_form.is_valid() and room_formset.is_valid():
#             main_request = main_form.save()
#             room_instances = room_formset.save(commit=False)

#             for room_instance in room_instances:
#                 room_instance.quotation_id = main_request
#                 room_instance.save()

#     context = {
#         'main_form': main_form,
#         'room_formset': room_formset,
#     }

#     return render(request, 'quotation/create_quotation.html', context)


class HotelViewSet(StatusFieldMixin, viewsets.ModelViewSet):
    # different serializer depending on usage (performance reasons)
    def get_serializer_class(self):
        # print(self.action)
        if self.action == "create":
            return serializers_quotation.HotelItemSerializer
        if self.action == "list":
            return serializers_quotation.HotelListSerializer
        if self.action == "partial_update":
            return serializers_quotation.HotelItemSerializer
        return serializers_quotation.HotelItemSerializer

    def get_queryset(self):
        # limit API list to objects that the user should be able to see - operation per item is arranged in permissions file
        employee = models_quotation.Employee.objects.get(
            user=self.request.user)
        
        print(employee)
        #TODO
        # if employee.hotel_staff: 
        #     Hotel = models_quotation.Hotel.objects.filter(hotel=client)
        # if employee.company_staff:
        #     Hotel = models_quotation.Hotel.objects.filter(hotel=client)

        client = employee.client
  
        Hotel = models_quotation.Hotel.objects.all()

        # # filter optional get parameters after permissions check
        # HotelRatenames = self.request.GET.getlist('name')
        # if (len(HotelRatenames) > 0 and len(HotelRates) > 0):
        #     HotelRatename = HotelRatenames[0]
        #     HotelRates = HotelRates.filter(name=HotelRatename)

        # return
        return (Hotel)  # .order_by('id')


class HotelRateViewSet(StatusFieldMixin, viewsets.ModelViewSet):
    # different serializer depending on usage (performance reasons)
    def get_serializer_class(self):
        # print(self.action)
        if self.action == "create":
            return serializers_quotation.HotelRateItemSerializer
        if self.action == "list":
            return serializers_quotation.HotelRateListSerializer
        if self.action == "partial_update":
            return serializers_quotation.HotelRateItemSerializer
        return serializers_quotation.HotelRateItemSerializer

    def get_queryset(self):
        # limit API list to objects that the user should be able to see - operation per item is arranged in permissions file
        # employee = models_quotation.Employee.objects.get(
        #     user=self.request.user)
        # client = employee.client
        # HotelRates = models_quotation.HotelRate.objects.filter(
        #     client=client)
        HotelRates = models_quotation.HotelRate.objects.all()

        # # filter optional get parameters after permissions check
        # HotelRatenames = self.request.GET.getlist('name')
        # if (len(HotelRatenames) > 0 and len(HotelRates) > 0):
        #     HotelRatename = HotelRatenames[0]
        #     HotelRates = HotelRates.filter(name=HotelRatename)

        # return
        return (HotelRates.order_by('id'))


class CompanyViewSet(StatusFieldMixin, viewsets.ModelViewSet):
    # different serializer depending on usage (performance reasons)
    def get_serializer_class(self):
        # print(self.action)
        if self.action == "create":
            return serializers_quotation.CompanyItemSerializer
        if self.action == "list":
            return serializers_quotation.CompanyListSerializer
        if self.action == "partial_update":
            return serializers_quotation.CompanyItemSerializer
        return serializers_quotation.CompanyItemSerializer

    def get_queryset(self):
        # limit API list to objects that the user should be able to see - operation per item is arranged in permissions file
        # employee = models_quotation.Employee.objects.get(
        #     user=self.request.user)
        # client = employee.client
        # Companys = models_quotation.Company.objects.filter(
        #     client=client)
        Companys = models_quotation.Company.objects.all()

        # # filter optional get parameters after permissions check
        # Companynames = self.request.GET.getlist('name')
        # if (len(Companynames) > 0 and len(Companys) > 0):
        #     Companyname = Companynames[0]
        #     Companys = Companys.filter(name=Companyname)

        # return
        return (Companys.order_by('id'))