# Generated by Django 4.2.5 on 2023-09-21 16:07

from django.db import migrations
import zcore.core.storage_utils


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0003_themesmodel_created_at_themesmodel_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenantmodel",
            name="fav_icon",
            field=zcore.core.storage_utils.ZFileField(
                blank=True,
                null=True,
                upload_to=zcore.core.storage_utils.RandomUniqueFileName,
                validators=[zcore.core.storage_utils.validate_file_extension],
                verbose_name="Fav Icon",
            ),
        ),
        migrations.AlterField(
            model_name="tenantmodel",
            name="logo",
            field=zcore.core.storage_utils.ZFileField(
                blank=True,
                null=True,
                upload_to=zcore.core.storage_utils.RandomUniqueFileName,
                validators=[zcore.core.storage_utils.validate_file_extension],
                verbose_name="Logo",
            ),
        ),
    ]
