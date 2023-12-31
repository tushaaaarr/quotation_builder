# Generated by Django 4.2.1 on 2023-06-20 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0030_quotationmainrequest_area_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='Company_footer',
            new_name='company_footer',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='Company_header',
            new_name='company_header',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='Company_logo',
            new_name='company_logo',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='Company_logo_watermark',
            new_name='company_logo_watermark',
        ),
        migrations.AlterField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='quotation.company'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='quotation.hotel'),
        ),
    ]
