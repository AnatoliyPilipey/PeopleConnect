# Generated by Django 5.0.6 on 2024-06-26 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="user_pk",
        ),
    ]