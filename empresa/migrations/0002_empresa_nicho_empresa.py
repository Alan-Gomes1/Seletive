# Generated by Django 4.2.2 on 2023-06-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='nicho_empresa',
            field=models.CharField(choices=[('M', 'Marketing'), ('SF', 'Setor Financeiro'), ('T', 'Tecnologia')], default=1, max_length=3),
            preserve_default=False,
        ),
    ]
