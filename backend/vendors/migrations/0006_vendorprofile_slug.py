from django.db import migrations, models


def generate_unique_slug(apps, schema_editor):
    VendorProfile = apps.get_model('vendors', 'VendorProfile')
    for vendor in VendorProfile.objects.all():
        if vendor.slug:
            continue
        base_slug = vendor.shop_name.lower().replace(' ', '-')[:150]
        slug = base_slug
        index = 1
        while VendorProfile.objects.filter(slug=slug).exclude(pk=vendor.pk).exists():
            slug = f"{base_slug}-{index}"
            index += 1
        vendor.slug = slug
        vendor.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0005_remove_vendorprofile_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='slug',
            field=models.SlugField(blank=True, max_length=160, null=True, unique=True),
        ),
        migrations.RunPython(generate_unique_slug, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='vendorprofile',
            name='slug',
            field=models.SlugField(blank=True, max_length=160, unique=True, null=True),
        ),
    ]
