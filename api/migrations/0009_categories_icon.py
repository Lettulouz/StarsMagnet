# Generated by Django 4.2.1 on 2023-06-02 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_categories_categoriesofcompanies'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='icon',
            field=models.CharField(default='exit', max_length=55),
            preserve_default=False,
        ),
    ]