# Generated by Django 4.0 on 2022-06-26 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetail',
            name='auth_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='doctor_detail', to='auth.user'),
        ),
    ]
