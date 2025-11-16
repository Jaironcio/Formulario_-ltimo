# Generated manually to add slug field with proper data migration

from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    """Populate slugs for existing Centro records"""
    Centro = apps.get_model('incidencias', 'Centro')
    for centro in Centro.objects.all():
        if not centro.slug:
            centro.slug = slugify(centro.nombre)
            centro.save()


def reverse_populate_slugs(apps, schema_editor):
    """Reverse migration - clear slugs"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0002_operario_incidencia'),
    ]

    operations = [
        # Step 1: Add slug field as nullable (without unique constraint)
        migrations.AddField(
            model_name='centro',
            name='slug',
            field=models.SlugField(max_length=100, null=True, blank=True),
        ),
        
        # Step 2: Populate slugs for existing records
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
        
        # Step 3: Make slug field unique and non-nullable
        migrations.AlterField(
            model_name='centro',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, blank=True),
        ),
    ]
