from tkinter import Image

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cars, Brands, CarCompartments, Details, Key, DetailsInformation, DetailFiles
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import AuthLoginForm, UserRegistrationForm, UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import utils
from reportlab.lib.utils import ImageReader
from io import BytesIO
import pandas as pd
from django.contrib.auth.models import Group


# Be continued


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf(request, brand_slug, compartment_id, detail_slug):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="detail.pdf"'
    detail = get_object_or_404(Details, slug=detail_slug)
    detailInform = DetailsInformation.objects.all().filter(brand__slug=brand_slug,
                                                           compartment__id=compartment_id,
                                                           detail__slug=detail_slug)
    doc = SimpleDocTemplate(response, pagesize=letter, title='Detail: ' + detail.name)
    styles = getSampleStyleSheet()

    elements = []
    pdfmetrics.registerFont(TTFont('Times-roman', 'main/static/Times New Roman Regular.ttf'))
    russian_font = 'Times-roman'
    styles['Normal'].fontName = russian_font
    styles['Title'].fontName = russian_font

    elements.append(Paragraph(detail.name, styles['Title']))


    i = 1
    for data in detailInform:
        elements.append(Paragraph(str(i) + ')  ' + 'Part Name:  ' + str(data.partName), styles['Normal']))
        elements.append(Paragraph('Part Number: ' + str(data.partNumber), styles['Normal']))
        elements.append(Paragraph('L/R:  ' + data.LR, styles['Normal']))
        elements.append(Paragraph('QTY:  ' + str(data.QTY), styles['Normal']))
        elements.append(Paragraph('Remarks:  ' + str(data.Remarks), styles['Normal']))

        elements.append(Spacer(1,12))
        i+=1
    doc.build(elements)
    print(request.COOKIES['sessionid'])
    return response


class SearchResultsView(ListView):
        model = Details or Brands
        template_name = 'main/search.html'

        def get_context_data(self, **kwargs):
            query = self.request.GET.get('detail')
            messages.error(self.request, ('Not found any details for your requst!'))
            object_list = Details.objects.filter(
                Q(slug__icontains=query) | Q(name__icontains=query) | Q(identifier__icontains=query))
            print(object_list)
            context = {
                'object_list': object_list,
            }
            return context


@login_required
@transaction.atomic
def ipdate_profile(request):
    group = request.user.groups.filter(name='Сотрудники' or 'Сотрудник' or 'сотрудники' or 'ishchilar')
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if group:
            if user_form.is_valid() and profile_form.is_valid():
                profile_form.save()
                user_form.save()
                messages.success(request, ('Your profile was successfully updated '))
                return redirect('home')
            else:
                messages.error(request, ('Please to solve incorrect information'))
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, ('Your profile was successfully updated'))
                return redirect('home')
            else:
                messages.error(request, ('Please to solve incorrect information'))
    else:
        group2 = request.user.groups.filter(name='Сотрудники')
        group1 = request.user.groups.filter(name='Админы')
        group3 = request.user.groups.filter(name='Xodimlar')
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'group1': group1,
        'group2': group2,
        'group3': group3,
    })


class AuthLoginView(LoginView):
    template_name = 'main/auth.html'
    form_class = AuthLoginForm
    success_url = reverse_lazy('home')
    success_message = 'Congratulation you were authenticated successfully! '
    error_message = 'Error with authentication process, please try again! '

    def get_success_url(self):
        return self.success_url


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy('login')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print(request.POST['password'])
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            group_employee = Group.objects.get(name="Сотрудники")
            group_employee.user_set.add(new_user)

            messages.success(request, "Congratulation you were registered successfully")
            return redirect('home')
        else:
            messages.error(request, ('Any information was incorrectly!'))
            return redirect('registration')
    else:
        template = 'main/registration.html'
        context = {

        }
        return render(request, template, context)


def checkKey(request):
    if request.method == 'POST':
        keys = Key.objects.all().order_by('-date_create')
        for key in keys:
            if request.POST['key'] == key.password:
                return redirect('registration')
            else:
                messages.error(request, ('Key password was written incorrectly!'))
                return redirect('checkKey')
    else:
        template = 'main/checkKey.html'
        context = {}
        return render(request, template, context)


def index(request):
    if request.user.is_authenticated:
        templates = 'main/index.html'
        cars = Cars.objects.all()
        context = {
            'name': 'John',
            'cars': cars,


        }

        return render(request, templates, context)
    else:
        return redirect('login')


def brands(request, car_slug):
    if request.user.is_authenticated:
        templates = 'main/brands.html'
        car = get_object_or_404(Cars, slug=car_slug)
        brands = Brands.objects.all().filter(car__slug=car.slug)
        context = {
            'brands': brands,
            'car': car,
        }
        return render(request, templates, context)
    else:
        return redirect('login')


def compartments(request, car_slug, brand_slug):
    if request.user.is_authenticated:
        templates = 'main/compartment.html'
        car = get_object_or_404(Cars, slug=car_slug)
        brand = get_object_or_404(Brands, slug=brand_slug)
        compartments = CarCompartments.objects.all().filter(car__slug=car_slug)
        context = {
            'car': car,
            'brand': brand,
            'compartments': compartments,
        }
        return render(request, templates, context)
    else:
        return redirect('login')


def details(request, car_slug, brand_slug, compartment_id):
    if request.user.is_authenticated:
        templates = 'main/details.html'
        car = get_object_or_404(Cars, slug=car_slug)
        brand = get_object_or_404(Brands, slug=brand_slug)
        compartment = get_object_or_404(CarCompartments, id=compartment_id)
        details = Details.objects.all().filter(compartment__id=compartment_id, brand__slug=brand_slug)
        context = {
            'car': car,
            'brand': brand,
            'compartment': compartment,
            'details': details,
        }
        return render(request, templates, context)
    else:
        return redirect('login')


def detailInform(request, car_slug, brand_slug, compartment_id, detail_slug):
    global long, df, data, files_1, files_2
    if request.user.is_authenticated:
            group = request.user.groups.filter(name='Сотрудники')
            group2 = request.user.groups.filter(name='Xodimlar')
            group3 = request.user.groups.filter(name='Админы')
            if group or group2 or group3:
                    partNumber = request.POST.get('element')
                    elements = DetailsInformation.objects.all().filter(partNumber=partNumber, detail__slug=detail_slug)
                    detailsInformation = DetailsInformation.objects.all().filter(detail__slug=detail_slug,
                                                                                 compartment__id=compartment_id,
                                                                                 brand__slug=brand_slug)
                    detailsInformation = list(detailsInformation)
                    detailsInformation = sorted(
                        detailsInformation,
                        key=lambda x: int(''.join(filter(str.isdigit, x.item)) or 0)
                    )
                    car = get_object_or_404(Cars, slug=car_slug)
                    brand = get_object_or_404(Brands, slug=brand_slug)
                    compartment = get_object_or_404(CarCompartments, id=compartment_id)
                    templates = 'main/detailInform.html'
                    detail = get_object_or_404(Details, slug=detail_slug)
                    files = DetailFiles.objects.all().filter(brand__slug=brand_slug, compartment__id=compartment_id,
                                                             detail__slug=detail_slug)
                    list_file = []
                    files_2 = []
                    files_1 = []
                    for file in files:
                        list_file.append(file)
                    if len(list_file) < 2:
                        files_1 = list_file
                    else:
                        index = len(list_file) - 1
                        files_2 = list_file[index]
                    context = {
                        'car': car,
                        'brand': brand,
                        'compartment': compartment,
                        'detail': detail,
                        'detailsInformation': detailsInformation,
                        'elements': elements,
                        'files': files_1,
                        'file': files_2,

                        }
                    return render(request, templates, context)
            else:
                car = get_object_or_404(Cars, slug=car_slug)
                brand = get_object_or_404(Brands, slug=brand_slug)
                compartment = get_object_or_404(CarCompartments, id=compartment_id)
                return redirect('details', car.slug, brand.slug, compartment.id)

    else:
        return redirect('login')


def elementPhoto(request, element_id):
    if request.user.is_authenticated:
        template = 'main/photo_element.html'
        element = get_object_or_404(DetailsInformation, id=element_id)
        context = {
                'element': element,
            }
        return render(request, template, context)
    else:
        return redirect('login')
