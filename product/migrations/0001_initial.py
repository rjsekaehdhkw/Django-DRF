# Generated by Django 3.2.13 on 2022-06-24 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='product/thumbnail', verbose_name='썸네일')),
                ('description', models.TextField(verbose_name='설명')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('exposure_end_date', models.DateField(verbose_name='노출 종료 일자')),
                ('is_active', models.BooleanField(verbose_name='활성화 여부')),
                ('price', models.IntegerField(verbose_name='가격')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='내용')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('rating', models.IntegerField(verbose_name='평점')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product', verbose_name='상품')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
    ]
