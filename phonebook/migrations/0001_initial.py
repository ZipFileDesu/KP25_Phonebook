# Generated by Django 2.2.1 on 2019-06-10 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=200)),
                ('city_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.City')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(default=None, max_length=200, null=True)),
                ('city_phone', models.CharField(default=None, max_length=200, null=True)),
                ('ip_phone', models.CharField(default=None, max_length=200, null=True)),
                ('department', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Department')),
                ('position', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Position')),
                ('region', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Region')),
            ],
        ),
    ]
