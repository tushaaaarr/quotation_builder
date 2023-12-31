# Generated by Django 4.2.1 on 2023-06-03 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0014_remove_quotationmainrequest_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationroomrequest',
            name='package_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='package_type_requests', to='quotation.hotelrate'),
            preserve_default=False,
        ),
    ]
