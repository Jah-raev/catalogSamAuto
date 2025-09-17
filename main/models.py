from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Cars(models.Model):
    name = models.CharField(max_length=200, verbose_name='Вид Т/С')
    slug = models.SlugField(max_length=200, verbose_name='Идентификатор')
    img = models.ImageField(upload_to='media/cars', blank=True, null=True, verbose_name='Фото Машины')
    dateCreate = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата добовление')
    dateUpdate = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Дата изменение')

    class Meta:
        verbose_name = 'Вид Т/С'
        verbose_name_plural = 'Виды Т/С'

    def __str__(self):
        return self.name


class Brands(models.Model):
    name = models.CharField(max_length=200, verbose_name='Модели машины')
    slug = models.SlugField(max_length=200, verbose_name='Идентификатор')
    inform = models.TextField(verbose_name='Информация о бренде ')
    img = models.ImageField(upload_to='brands', blank=True, null=True, verbose_name='Фото')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name='Тип машины')
    date_create = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return self.name


class CarCompartments(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Названия отсека ')
    slug = models.SlugField(max_length=200, verbose_name='Идентификатор')
    img = models.ImageField(upload_to='CarCompartments', blank=True, null=True, verbose_name='Фото отсека')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE,  verbose_name='Тип машины')
    date_create = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания ')
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Отсек машины'
        verbose_name_plural = 'Отсеки машины'

    def __str__(self):
        return self.name


class Details(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Названия деталя')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Идентификатор')
    identifier = models.CharField(max_length=200, verbose_name='Номер детали')
    price = models.CharField(max_length=200, verbose_name='Цена')
    brand = models.ForeignKey(Brands, models.CASCADE, verbose_name='Модель машины')
    compartment = models.ForeignKey(CarCompartments, models.CASCADE, verbose_name='Отсек машины')
    img = models.ImageField(upload_to='Details', null=True, blank=True, verbose_name='Фото деталя')
    imgDetails = models.ImageField(upload_to='DetailsDescriptions', null=True,
                                   blank=True, verbose_name='Фото подробного описания деталя')
    date_create = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        return self.name


class DetailsInformation(models.Model):
    partName = models.CharField(max_length=200, verbose_name='Название партии')
    partNumber = models.CharField(max_length=200, verbose_name='Номер партии')
    item = models.CharField(max_length=200, verbose_name='Элемент')
    LR = models.CharField(max_length=200, verbose_name='LR')
    QTY = models.IntegerField(verbose_name='Количество')
    Remarks = models.TextField(verbose_name='Замечание')
    detail = models.ForeignKey(Details, on_delete=models.CASCADE, verbose_name='Деталь ')
    compartment = models.ForeignKey(CarCompartments, on_delete=models.CASCADE, verbose_name='Отсек машины')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='Модель ТС')
    # file = models.FileField(upload_to='detail_files', blank=True, null=True, verbose_name='Excel файл')
    img = models.ImageField(upload_to='DetailsDescriptions', null=True, blank=True, verbose_name='Фото элемента')

    class Meta:
        verbose_name = 'Информация о партии деталя'
        verbose_name_plural = 'Информации о партиях деталей'

    def __str__(self):
        return self.partName


class DetailFiles(models.Model):
    name = models.CharField(max_length=200, verbose_name='Источник')
    file = models.FileField(upload_to='detailFiles/', verbose_name='Файл')
    # file_excel = models.FileField(upload_to='detailFiles/excels', blank=True, null=True, verbose_name='Файл excel')
    detail = models.ForeignKey(Details, on_delete=models.CASCADE, verbose_name='Деталь')
    compartment = models.ForeignKey(CarCompartments, on_delete=models.CASCADE, verbose_name='Название отсека')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='Модель ТС')
    date_create = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Файл деталя'
        verbose_name_plural = 'Файлы деталей'

    def __str__(self):
        return self.name


class Key(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    password = models.CharField(max_length=200, verbose_name='Новый ключ пароль')
    date_create = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создния')
    date_update = models.DateTimeField(auto_now=True, null=True,blank=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    department = models.CharField(max_length=200, verbose_name='Департамент')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phoneNumber = models.CharField(max_length=200, verbose_name='Телефонный номер')
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Информация о сотруднике'
        verbose_name_plural = 'Информации о сотрудниках'


# Это декоратор отвечает за проверку у пользователья есть профайл или нет
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # проверяет  профайл создан или нет в случаи усли да создается связь между Profile and User
    if created:
        Profile.objects.create(user=instance)
    else:
        # В противном случаи идет сюда где создается пустой Profile for user
        instance.profile.save()


# In here take place saving any changing in profile
@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    # if User.profile:
    instance.profile.save()
    # else:
    #      Profile.object.create(user=instance)