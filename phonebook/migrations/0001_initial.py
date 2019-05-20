# Generated by Django 2.2.1 on 2019-05-19 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch_Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_office_region_number', models.IntegerField()),
                ('branch_office_name', models.CharField(max_length=200)),
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
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('city_phone', models.CharField(max_length=200)),
                ('ip_phone', models.CharField(max_length=200)),
                ('branch_office', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Branch_Office')),
                ('department', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Department')),
                ('position', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.Position')),
            ],
        ),
    ]
