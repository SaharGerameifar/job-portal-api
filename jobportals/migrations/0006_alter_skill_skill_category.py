# Generated by Django 3.2.13 on 2006-01-03 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobportals', '0005_remove_educationalbackground_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportals.skillcategory'),
        ),
    ]
