from django.db import migrations
from django.utils.text import slugify

CATEGORIES = [
    'Backend',
    'Frontend',
    'AI',
    'Cyber Security',
    'Cyber Sport',
    'Game Development',
]


def add_categories(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    for name in CATEGORIES:
        base_slug = slugify(name)
        # If exact name already exists, skip
        if Category.objects.filter(name=name).exists():
            continue
        # If slug already taken (maybe with another name), skip to avoid collisions
        if Category.objects.filter(slug=base_slug).exists():
            continue
        # Ensure unique slug just in case
        final_slug = base_slug
        i = 1
        while Category.objects.filter(slug=final_slug).exists():
            i += 1
            final_slug = f"{base_slug}-{i}"
        Category.objects.create(name=name, slug=final_slug)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    Category.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RunPython(add_categories, reverse_code=remove_categories),
    ]


