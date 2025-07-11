# Generated by Django 5.2 on 2025-04-26 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0005_alter_card_order'),
        ('users', '0002_rename_manageteampermission_role_manageteampermission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='cardID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health.card'),
        ),
        migrations.AddField(
            model_name='vote',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='userID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
