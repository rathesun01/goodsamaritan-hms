# Generated by Django 4.0 on 2022-06-23 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=16)),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.user')),
            ],
        ),
    ]
