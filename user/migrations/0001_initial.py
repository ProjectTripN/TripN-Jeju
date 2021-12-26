# Generated by Django 3.2.5 on 2021-12-26 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.BooleanField()),
                ('mbti', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='image.category')),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=20)),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('birth', models.DateField()),
                ('gender', models.TextField()),
                ('mbti', models.TextField()),
                ('mbti_list', models.TextField()),
                ('card_number', models.TextField()),
                ('card_company', models.IntegerField()),
                ('reg_date', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='image.category')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='image.image')),
                ('person_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.person')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
