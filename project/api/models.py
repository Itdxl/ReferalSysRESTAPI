from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    referal_code = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'


class ReferalCode(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    expiration_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Referal Codes'


class ReferalHistory(models.Model):
    # someone who created referal code
    ref_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referals_creator')
    # someone who used referal code
    ref_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referals_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Referal Histories'
