# Generated by Django 4.2.1 on 2023-06-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0032_quotationroomrequest_error_msg_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationroomrequest',
            name='error_msg',
        ),
        migrations.RemoveField(
            model_name='quotationroomrequest',
            name='pdf_file',
        ),
        migrations.RemoveField(
            model_name='quotationroomrequest',
            name='status',
        ),
        migrations.RemoveField(
            model_name='quotationroomrequest',
            name='url',
        ),
        migrations.AddField(
            model_name='quotationmainrequest',
            name='error_msg',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='quotationmainrequest',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs'),
        ),
        migrations.AddField(
            model_name='quotationmainrequest',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('G', 'Generating'), ('R', 'Ready'), ('E', 'Error')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='quotationmainrequest',
            name='url',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
