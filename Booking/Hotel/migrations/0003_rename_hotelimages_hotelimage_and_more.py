# Generated by Django 4.1.5 on 2023-01-22 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_remove_amenities_created_at_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HotelImages',
            new_name='HotelImage',
        ),
        migrations.AlterModelOptions(
            name='amenities',
            options={'verbose_name_plural': 'Amenities'},
        ),
    ]