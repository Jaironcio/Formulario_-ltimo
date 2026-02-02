from django.db import migrations
from django.utils.text import slugify


def seed_centros(apps, schema_editor):
    Centro = apps.get_model('incidencias', 'Centro')

    nombres = [
        'Trafún',
        'Liquiñe',
        'Cipreses',
        'Santa Juana',
        'Rahue',
        'Esperanza',
        'Hueyusca',
        'PCC',
    ]

    for nombre in nombres:
        slug = slugify(nombre)
        defaults = {'nombre': nombre}
        # En la migración histórica, el save() del modelo no se ejecuta,
        # por lo que debemos setear id/slug explícitamente para evitar PK vacía.
        if hasattr(Centro, 'slug'):
            defaults['slug'] = slug
        Centro.objects.get_or_create(id=slug, defaults=defaults)


def unseed_centros(apps, schema_editor):
    Centro = apps.get_model('incidencias', 'Centro')

    nombres = [
        'Trafún',
        'Liquiñe',
        'Cipreses',
        'Santa Juana',
        'Rahue',
        'Esperanza',
        'Hueyusca',
        'PCC',
    ]

    slugs = [slugify(n) for n in nombres]
    Centro.objects.filter(id__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0011_monitoreosensores_hora_inicio'),
    ]

    operations = [
        migrations.RunPython(seed_centros, reverse_code=unseed_centros),
    ]
