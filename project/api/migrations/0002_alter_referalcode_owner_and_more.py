# Generated by Django 5.0.2 on 2024-03-12 20:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='referalcode',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='referalhistory',
            name='ref_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referals_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='referalhistory',
            name='ref_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referals_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='referalcode',
            options={'verbose_name_plural': 'Referal Codes'},
        ),
        migrations.AlterModelOptions(
            name='referalhistory',
            options={'verbose_name_plural': 'Referal Histories'},
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
