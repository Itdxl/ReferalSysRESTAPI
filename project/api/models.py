from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ReferalCode(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    expiration_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Referal Codes'

    def __str__(self):
        return self.name


class ReferalHistory(models.Model):
    # someone who created referal code
    ref_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referals_creator')
    # someone who used referal code
    ref_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referals_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Referal Histories'

    def __str__(self):
        return f'\'{self.ref_user}\' registred with  \'{self.ref_creator}\'s code'
