# Generated by Django 4.2.6 on 2023-10-25 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0006_customer_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="status",
        ),
    ]
