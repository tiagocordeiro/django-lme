# Generated by Django 2.1.2 on 2018-10-25 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LondonMetalExchange',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('cobre', models.DecimalField(decimal_places=2, max_digits=20)),
                ('zinco', models.DecimalField(decimal_places=2, max_digits=20)),
                ('aluminio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('chumbo', models.DecimalField(decimal_places=2, max_digits=20)),
                ('estanho', models.DecimalField(decimal_places=2, max_digits=20)),
                ('niquel', models.DecimalField(decimal_places=2, max_digits=20)),
                ('dolar', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'verbose_name_plural': 'cotação',
            },
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cash', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='serie',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TimeSerie'),
        ),
    ]
