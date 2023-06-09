# Generated by Django 3.2.19 on 2023-05-27 11:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('E_Library', '0012_auto_20230527_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Published', 'Published'), ('Pending', 'Pending')], default='Pending', max_length=9),
        ),
        migrations.AlterField(
            model_name='rating',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='E_Library.book'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL),
        ),
    ]
