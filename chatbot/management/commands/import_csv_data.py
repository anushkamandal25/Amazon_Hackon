# myapp/management/commands/import_csv_data.py

from django.core.management.base import BaseCommand
import pandas as pd

import os
import sys

# Get the current directory (location of importfile.py)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Append the parent directory (the location of your app) to the Python path
parent_directory = os.path.dirname(current_directory)
app_directory = os.path.join(parent_directory, 'core')
csv_file_paths= os.path.join(current_directory, '../../../dataset/sampledata.csv')
if app_directory not in sys.path:
    sys.path.append(app_directory)

# Now, you can import your models
from core.models import Product  # Replace 'YourModel' with the actual model name


class Command(BaseCommand):
    help = 'Import product data from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = csv_file_paths
        data = pd.read_csv(csv_file_path)

        # Iterate through the CSV data and create database records
        for _, row in data.iterrows():
            product = Product(
                name=row['name'],
                price=row['price'],
                rating=row['rating']
                # Add other fields as needed
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Imported product: {product.name}'))

