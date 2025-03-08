import csv
import json
import os
import django
from pathlib import Path
import sys
from django.conf import settings
# Add the project directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()
from prdcatalog.models import Product,Category
def load_products():
    base_dir = Path(__file__).resolve().parent.parent
    csv_file = base_dir / 'products.csv'
    csv_file = os.path.join(settings.BASE_DIR, 'products.csv')
    products_loaded = 0
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)            
            Product.objects.all().delete()    
            for row in csv_reader:
                cat = row['categories']
                try:
                    product = Product(
                        # product_id=row['ProductId'],
                        name=row['title'],
                        desp=row['description'],
                        in_price = row['initial_price'],
                        fn_price = row['final_price'],
                        brand=row['brand'],
                        reviews=row['reviews_count'],
                        # color=row['Colour'],
                        # usage=row['Usage'],
                        
                        # image=row['Image'],
                        img=row['image_url']
                    )
                    # we need to save at first stage to get the id and to add category field next.
                    product.save() 
                    if(cat):
                        try:
                            cats = json.loads(cat)
                        except json.JSONDecodeError or Exception as e:
                            print("error while adding category",e)
                            continue
                        for c in cats:
                            cate,create = Category.objects.get_or_create(name=c.strip())
                            product.cat.add(cate)
                    product.save()
                    products_loaded += 1
                    # Print progress every 100 products
                    if products_loaded % 100 == 0:
                        print(f"Loaded {products_loaded} products...")
                        
                except Exception as e:
                    print(f"Error loading product {row['title']}: {str(e)}")
                    continue
                    
        print(f"\nSuccessfully loaded {products_loaded} products into the database!")
        
    except Exception as e:
        print(f"Error opening CSV file: {str(e)}")

if __name__ == "__main__":
    print("Starting product load process...")
    load_products()