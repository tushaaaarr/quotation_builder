from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from quotation import views as quotation_views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('index', views.index, name='index'),
    path('', views.home, name='home'),

    # path('login/', quotation_views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', quotation_views.RegisterView.as_view(), name='auth_register'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),

    # hotel side
    path('hotel/add/', views.add_hotel, name='add_hotel/'),
    path('hotel/<int:pk>/update/', views.update_hotel, name='update_hotel/'),
    path('hotel/list/', views.hotel_list, name='hotel_list'),

    # Hotel rate side
    path('hotelrate/add/', views.add_hotel_rate, name='add_hotel_rate/'),
    path('hotelrate/list/', views.hotelrate_list, name='hotelrate_list'),

    path('hotelrate/<int:pk>/update/', views.update_hotel_rate, name='update_hotel_rate/'),

    # company side   
    path('company/add/', views.add_company, name='add_company/'),
    path('company/<int:pk>/update/', views.update_company, name='update_company/'),
    path('company/list/', views.company_list, name='company_list'),

    # quotation things
    path('create_quotation/', views.create_quotation, name='create_quotation'),
    path('create-quotation/', views.create_quatation_new, name='create_quotation_copy'),
    path('get_form_data/', views.get_form_data, name='get_form_data'),
    # path('create_quatation_new22/', views.create_quatation_new22, name='create_quatation_new22'),



    # Add any additional URLs as needed
]



#### rest API ####
router = SimpleRouter()
router.register(
    r'hotel',
    quotation_views.HotelViewSet,
    basename='Hotel'
)
router.register(
    r'hotelrate',
    quotation_views.HotelRateViewSet,
    basename='HotelRate'
)
router.register(
    r'company',
    quotation_views.CompanyViewSet,
    basename='Company'
)