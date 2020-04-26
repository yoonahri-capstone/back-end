# Generated by Django 3.0.5 on 2020-04-26 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('folder_id', models.AutoField(primary_key=True, serialize=False)),
                ('folder_name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'folder_name')},
            },
        ),
        migrations.CreateModel(
            name='Scrap',
            fields=[
                ('scrap_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.URLField()),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scraps', to='memmem_app.Folder')),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('folder', 'url')},
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_text', models.CharField(max_length=30)),
                ('scrap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='memmem_app.Scrap')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='memmem_app/media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('memo_id', models.AutoField(primary_key=True, serialize=False)),
                ('memo', models.TextField()),
                ('scrap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memos', to='memmem_app.Scrap')),
            ],
        ),
    ]
