# Generated by Django 3.2.16 on 2024-02-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_subscription_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='field_a',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='subscription',
            name='field_b',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['field_a', 'field_b'], name='services_su_field_a_155836_idx'),
        ),
    ]
