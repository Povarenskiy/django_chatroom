# Generated by Django 4.1.3 on 2022-12-22 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websocket_app', '0004_chatroom_room_name_alter_message_chatroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='room_name',
        ),
    ]