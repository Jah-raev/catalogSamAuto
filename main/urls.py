from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:car_slug>/Brands', views.brands, name='brands'),
    path('<slug:car_slug>/Brands/<slug:brand_slug>/Compartments', views.compartments, name='compartments'),
    path('<slug:car_slug>/Brands/<slug:brand_slug>/Compartments/<int:compartment_id>/Details', views.details, name='details'),
    path('<slug:car_slug>/Brands/<slug:brand_slug>/Compartments/<int:compartment_id>/Details/<slug:detail_slug>',
         views.detailInform, name='detailInfo'),

    path('<int:element_id>/Photo', views.elementPhoto, name='elementPhoto')
    ,
    path('login/', views.AuthLoginView.as_view(), name='login'),
    path('registrationNewEmployees/', views.register, name='registration'),
    path('logout/', views.AuthLogoutView.as_view(), name='logout'),
    path('checkKey/', views.checkKey, name='checkKey'),
    path('profile/', views.ipdate_profile, name='profile'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('<slug:brand_slug>/<int:compartment_id>/<slug:detail_slug>/print', views.generate_pdf, name='print'),
    # path('set_language/<str:language_code>/', views.set_language, name='set_language'),
    # path('<slug:car_slug>/Brands/<slug:brand_slug>/Compartments/<int:compartment_id>/Details/<slug:detail_slug>',
    #      views.display_excel_data, name='display'),

]