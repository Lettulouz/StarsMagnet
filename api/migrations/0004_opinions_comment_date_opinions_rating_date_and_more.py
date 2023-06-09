# Generated by Django 4.2.1 on 2023-05-29 14:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_opinions_side_of_comment_companies_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinions',
            name='comment_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='opinions',
            name='rating_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opinions',
            name='response_date',
            field=models.DateTimeField(null=True),
        ),
    ]
