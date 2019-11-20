# Generated by Django 2.2.6 on 2019-11-20 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateField(default='2019-01-01'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('date', 'room')},
        ),
    ]
