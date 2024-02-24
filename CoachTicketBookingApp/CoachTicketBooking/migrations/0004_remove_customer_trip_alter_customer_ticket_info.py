# Generated by Django 5.0.1 on 2024-02-24 03:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoachTicketBooking', '0003_ticketseller_status_alter_ticket_seat_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='trip',
        ),
        migrations.AlterField(
            model_name='customer',
            name='ticket_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CoachTicketBooking.ticket'),
        ),
    ]
