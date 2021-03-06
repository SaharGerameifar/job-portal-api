# Generated by Django 3.2.13 on 2006-01-03 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobportals', '0002_auto_20060102_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalbackground',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_educationalbackground', to='jobportals.job'),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='studying',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
