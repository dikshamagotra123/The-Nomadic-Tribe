# Generated by Django 4.1.5 on 2023-01-29 20:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0004_rename_amenities_adventures_alter_adventures_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amenity_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Amenities',
            },
        ),
        migrations.AddField(
            model_name='hotel',
            name='review',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='hotel',
            name='amenities',
            field=models.ManyToManyField(to='Hotel.amenities'),
        ),
    ]
