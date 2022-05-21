# Generated by Django 4.0.4 on 2022-05-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0003_remove_subcategory_category_category_sub_cat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub_cat',
        ),
        migrations.AddField(
            model_name='category',
            name='sub_cat',
            field=models.ManyToManyField(blank=True, null=True, to='store_app.subcategory'),
        ),
    ]
