import os
import sys
import shutil
from pathlib import Path

# Ensure project root is on sys.path so Django can import `core` settings
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.utils.text import slugify
from shop.models import Category, Product

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_IMG_DIR = BASE_DIR / 'core' / 'static' / 'img' / 'new'
MEDIA_PRODUCTS_DIR = BASE_DIR / 'media' / 'photos' / 'products'
MEDIA_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

def copy_images():
    images = []
    if STATIC_IMG_DIR.exists():
        for i, p in enumerate(sorted(STATIC_IMG_DIR.glob('*'))):
            if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
                dest = MEDIA_PRODUCTS_DIR / f'prod_{i}{p.suffix}'
                try:
                    shutil.copyfile(p, dest)
                    images.append(dest.name)
                except Exception as e:
                    print('skip', p, e)
    return images


def create_categories():
    names = ['Men', 'Women', 'Accessories', 'New Arrivals']
    cats = []
    for n in names:
        slug = slugify(n)
        cat, _ = Category.objects.get_or_create(name=n, slug=slug)
        cats.append(cat)
    return cats


def create_products(images, categories, target=30):
    created = 0
    img_count = len(images)
    i = 0
    while created < target:
        cat = categories[i % len(categories)]
        img_name = images[i % img_count] if img_count else ''
        name = f'{cat.name} Product {created+1}'
        slug = slugify(name)
        price = 19.99 + (created % 10) * 5
        stock = 10 + (created % 20)
        # Only create unique names/slugs
        if Product.objects.filter(slug=slug).exists():
            i += 1
            created += 1
            continue
        p = Product(
            category=cat,
            name=name,
            slug=slug,
            description=f'A sample {cat.name.lower()} product for demo purposes.',
            price=price,
            discount=0.00,
            stock=stock,
            new=(created % 3 == 0),
            is_available=True,
        )
        # assign image path relative to MEDIA_ROOT
        if img_name:
            p.image.name = f'photos/products/{img_name}'
        p.save()
        created += 1
        i += 1
    return created


def main():
    print('Copying source images...')
    images = copy_images()
    print('Found images:', images[:10])
    cats = create_categories()
    print('Categories:', [c.name for c in cats])
    created = create_products(images, cats, target=50)
    print(f'Created {created} products')


if __name__ == '__main__':
    main()
