from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("Login обязателен")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField("ID", primary_key=True)

    login = models.CharField("Логин", max_length=128, unique=True)
    password = models.CharField("Пароль", max_length=128)
    lname = models.CharField("Фамилия", max_length=128)
    fname = models.CharField("Имя", max_length=128)
    patronimyc = models.CharField("Отчество", max_length=128, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=12, unique=True)

    is_active = models.BooleanField("Активен", default=True)
    is_archive = models.BooleanField("В архиве", default=False)

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("dispatcher", "Dispatcher"),
    ]
    role = models.CharField(
        "Роль",
        max_length=16,
        choices=ROLE_CHOICES,
        default="dispatcher",
    )

    objects = UserManager()

    USERNAME_FIELD = "login"     
    REQUIRED_FIELDS = []          

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.lname} {self.fname}"


class Driver(models.Model):
    driver_id = models.AutoField("ID", primary_key=True)

    lname = models.CharField("Фамилия", max_length=128)
    fname = models.CharField("Имя", max_length=128)
    patronimyc = models.CharField("Отчество", max_length=128, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=12, unique=True)

    car_model = models.CharField("Модель авто", max_length=128)
    car_number = models.CharField("Номер авто", max_length=8)

    STATUS_CHOICES = [
        ("В ожидании", "В ожидании"),
        ("В работе", "В работе"),
        ("Вне работы", "Вне работы"),
    ]
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=STATUS_CHOICES,
        default="В ожидании",
    )

    is_blacklist = models.BooleanField("В чёрном списке", default=False)
    is_archive = models.BooleanField("В архиве", default=False)

    class Meta:
        db_table = "drivers"
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return f"{self.lname} {self.fname}"


class Client(models.Model):
    client_id = models.AutoField("ID", primary_key=True)

    lname = models.CharField("Фамилия", max_length=128)
    fname = models.CharField("Имя", max_length=128)
    patronimyc = models.CharField("Отчество", max_length=128, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=12, unique=True)

    is_blacklist = models.BooleanField("В чёрном списке", default=False)

    class Meta:
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.lname} {self.fname}"


class Shift(models.Model):
    shift_id = models.AutoField("ID", primary_key=True)

    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="shifts",
        verbose_name="Водитель",
    )

    start_shift = models.DateTimeField("Начало смены")
    end_shift = models.DateTimeField("Конец смены")

    opened_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opened_shifts",
        verbose_name="Открыл пользователь",
    )

    closed_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="closed_shifts",
        verbose_name="Закрыл пользователь",
    )

    class Meta:
        db_table = "shifts"
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    def __str__(self):
        return f"Смена {self.driver} с {self.start_shift} по {self.end_shift}"


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    base_coefficient = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = "districts"
        verbose_name = "Район"
        verbose_name_plural = "Районы"

    def __str__(self):
        return self.name


class Street(models.Model):
    street_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        db_column="fk_district_id",
        related_name="streets",
    )

    class Meta:
        db_table = "streets"
        verbose_name = "Улица"
        verbose_name_plural = "Улицы"

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class Tariff(models.Model):
    MONDAY = 1 << 0      
    TUESDAY = 1 << 1     
    WEDNESDAY = 1 << 2   
    THURSDAY = 1 << 3    
    FRIDAY = 1 << 4      
    SATURDAY = 1 << 5    
    SUNDAY = 1 << 6      

    DAYS_OF_WEEK_CHOICES = [
        (MONDAY, "Понедельник"),
        (TUESDAY, "Вторник"),
        (WEDNESDAY, "Среда"),
        (THURSDAY, "Четверг"),
        (FRIDAY, "Пятница"),
        (SATURDAY, "Суббота"),
        (SUNDAY, "Воскресенье"),
    ]

    tariff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time_from = models.TimeField()
    time_to = models.TimeField()
    days_of_week = models.IntegerField(
        help_text="Битовая маска дней недели: Пн=1, Вт=2, Ср=4, Чт=8, Пт=16, Сб=32, Вс=64"
    )
    is_archive = models.BooleanField("В архиве", default=False)

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name

    @classmethod
    def get_days_mask(cls, days_list):
        """Преобразует список дней в битовую маску."""
        mask = 0
        for day in days_list:
            mask |= day
        return mask

    def get_days_list(self):
        """Возвращает список дней недели для этого тарифа."""
        days = []
        for value, label in self.DAYS_OF_WEEK_CHOICES:
            if self.days_of_week & value:
                days.append(label)
        return days

    def get_days_display(self):
        """Возвращает строку с днями недели."""
        days = self.get_days_list()
        return ", ".join(days) if days else "Нет дней"