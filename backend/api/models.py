from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    ROLE_CHOICES = (
        ('elder', 'Elder'),
        ('volunteer', 'Volunteer'),
        ('superuser', 'Superuser')
        
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','role']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Cities(models.Model):
    title = models.CharField(max_length=255)
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    class Meta:
        managed = True  
        db_table = 'cities'
        
    def __str__(self):
        return f"{self.title} ({self.zipcode})"


class Activities(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'activities'
        
    def __str__(self):
        return self.name


class Elders(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    job = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Elder: {self.user.get_full_name()}"

    @property
    def age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class Volunteers(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    phone_number = models.CharField(max_length=20)
    url_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Volunteer: {self.user.get_full_name()}"


class Appointments(models.Model):
    date = models.DateTimeField()
    activity = models.ForeignKey(Activities, models.DO_NOTHING, related_name='appointments')
    elder = models.ForeignKey(Elders, models.DO_NOTHING, related_name='appointments')
    volunteer = models.ForeignKey(Volunteers, models.DO_NOTHING, related_name='appointments')

    class Meta:
        managed = True
        db_table = 'appointments'
        
    def __str__(self):
        return f"{self.activity.name} - {self.elder.user.name} & {self.volunteer.user.full_name}"