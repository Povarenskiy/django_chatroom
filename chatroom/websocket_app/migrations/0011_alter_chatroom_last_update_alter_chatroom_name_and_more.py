# Generated by Django 4.1.3 on 2023-02-06 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websocket_app', '0010_alter_message_options_chatroom_last_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='last_update',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='create',
            field=models.DateTimeField(),
        ),
    ]
