# Generated by Django 3.0.4 on 2020-03-27 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0003_auto_20200327_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloan',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Book'),
        ),
        migrations.AlterField(
            model_name='bookloan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]