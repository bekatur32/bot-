# Generated by Django 5.1.4 on 2025-01-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tovar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price_sng', models.PositiveIntegerField()),
                ('price_EUROPE_AMERICA', models.PositiveIntegerField()),
                ('price_Africa_Australia', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, default='products/default_image.png', null=True, upload_to='products/')),
                ('category', models.CharField(choices=[('fight_katan', 'Боевые катаны'), ('katan_replic', 'Не боевые катаны'), ('exclusive', 'экслюзвный товар')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
