# Generated by Django 2.2.3 on 2019-11-28 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('update', models.DateField(auto_now=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
