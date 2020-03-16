# Generated by Django 2.2 on 2019-05-13 08:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenAuthConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.TextField(help_text='Access Token')),
                ('prefix', models.CharField(blank=True, default='Bearer', help_text='Authentication Header Value Prefix', max_length=60)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('use_for_read', 'Allow to use for read operations'), ('use_for_write', 'Allow to use for write operations')),
            },
        ),
        migrations.CreateModel(
            name='SimpleAuthConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(help_text='Server Type', max_length=200)),
                ('password', fernet_fields.fields.EncryptedTextField(help_text='User Password')),
                ('auth_type', models.CharField(choices=[('BASIC', 'Basic Authentication'), ('DIGEST', 'Digest Authentication')], help_text='Authentication Type', max_length=6)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('use_for_read', 'Allow to use for read operations'), ('use_for_write', 'Allow to use for write operations')),
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('server_type', models.CharField(choices=[('ARCGIS_MSL', 'ArcGIS Map Server Layer'), ('ARCGIS_FSL', 'ArcGIS Feature Server Layer'), ('OGC-WMS', 'OGC Web Map Service'), ('OGC-WFS', 'OGC Web Feature Service'), ('GEONODE', 'Geonode'), ('GEOJSON', 'GeoJSON'), ('KML', 'KML'), ('POSTGIS', 'PostGIS')], help_text='Server Type', max_length=15)),
                ('title', models.CharField(help_text='Server Title', max_length=150)),
                ('url', models.TextField(help_text='Base Server URL', validators=[django.core.validators.URLValidator(schemes=['http', 'https', 'ftp', 'ftps', 'postgis'])])),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('operations', jsonfield.fields.JSONField(blank=True, default=dict)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
    ]