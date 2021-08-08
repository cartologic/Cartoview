# Generated by Django 2.2.20 on 2021-08-04 11:45

import cartoview.layer_attachments.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('layers', '0034_auto_20210329_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayerAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.IntegerField()),
                ('file', models.FileField(upload_to=cartoview.layer_attachments.models.get_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='layer_attachments', to=settings.AUTH_USER_MODEL)),
                ('layer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='layer_attachments', to='layers.Layer')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]