# Generated by Django 5.0.1 on 2024-02-29 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoachTicketBooking', '0011_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]