# Generated by Django 4.1.3 on 2022-12-02 12:42

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_story_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
