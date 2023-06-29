# Generated by Django 4.2.1 on 2023-06-03 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0008_remove_hotelrate_hotelname_companyhotelrate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='CompanyDescription',
            new_name='company_description',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='CompanyId',
            new_name='company_id',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='CompanyName',
            new_name='company_name',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='DateAdded',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='LastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='Username',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='CompanyStaff',
            new_name='company_staff',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='HotelStaff',
            new_name='hotel_staff',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='Username',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='AddressLine1',
            new_name='address_line1',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='Area',
            new_name='area',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='BedroomPic',
            new_name='bedroom_pic',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='Country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='DateAdded',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='DescriptionFirstDay',
            new_name='description_first_day',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='DescriptionFullDay',
            new_name='description_full_day',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='DescriptionLastDay',
            new_name='description_last_day',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='DiningRoomPic',
            new_name='diningroom_pic',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='HotelDescription',
            new_name='hotel_description',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='HotelId',
            new_name='hotel_id',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='HotelLogo',
            new_name='hotel_logo',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='HotelName',
            new_name='hotel_name',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='LastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='Username',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='AdultRate',
            new_name='adult_rate',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='ChildRate',
            new_name='child_rate',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='LastUpdated',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='DateApplicableFrom',
            new_name='date_applicable_from',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='DateApplicableTo',
            new_name='date_applicable_to',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='DateAdded',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='OldChildSharingRate',
            new_name='old_child_sharing_rate',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='PackageType',
            new_name='package_type',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='RateCurrency',
            new_name='rate_currency',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='RateSeason',
            new_name='rate_season',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='RateType',
            new_name='rate_type',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='Reference',
            new_name='reference',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='RoomCategory',
            new_name='room_category',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='RoomType',
            new_name='room_type',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='TravellerType',
            new_name='traveller_type',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='uniqueId',
            new_name='unique_id',
        ),
        migrations.RenameField(
            model_name='hotelrate',
            old_name='YoungChildSharingRate',
            new_name='young_child_sharing_rate',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='ReceptionRoomPic',
        ),
        migrations.RemoveField(
            model_name='hotelrate',
            name='HotelName',
        ),
        migrations.AddField(
            model_name='hotel',
            name='receptionroom_pic',
            field=models.ImageField(default='default_logo.jpg', upload_to='hotel_pics'),
        ),
        migrations.AddField(
            model_name='hotelrate',
            name='hotel_name',
            field=models.ManyToManyField(to='quotation.hotel'),
        ),
        migrations.DeleteModel(
            name='CompanyHotelRate',
        ),
    ]