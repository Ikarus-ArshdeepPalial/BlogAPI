import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.contrib.auth import get_user_model
from django.conf import settings
from blog.models import Blog
from PIL import Image

class Command(BaseCommand):
    help = 'Adds blogs from a CSV file.'

    def handle(self, *args, **options):
        email = input("Enter the email of the user to associate the blogs with: ")
        csv_file_path = input("Enter the path to the CSV file: ")

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f'User with email "{email}" does not exist.')

        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')

        dummy_image_path = self._get_dummy_image_path()

        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                blog = Blog(
                    user=user,
                    name=row.get('name'),
                    content=row.get('content'),
                )

                thumbnail_path = row.get('thumbnail')
                
                if thumbnail_path and os.path.exists(thumbnail_path):
                    with open(thumbnail_path, 'rb') as thumbnail_file:
                        blog.thumbnail.save(os.path.basename(thumbnail_path), File(thumbnail_file), save=False)
                else:
                    with open(dummy_image_path, 'rb') as dummy_file:
                        blog.thumbnail.save('dummy.jpg', File(dummy_file), save=False)
                
                blog.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added blog "{blog.name}"'))

        self.stdout.write(self.style.SUCCESS('Finished adding blogs from CSV.'))

    def _get_dummy_image_path(self):
        """Creates a dummy image if it does not exist and returns its path."""
        dummy_image_dir = os.path.join(settings.MEDIA_ROOT, 'defaults')
        os.makedirs(dummy_image_dir, exist_ok=True)
        dummy_image_path = os.path.join(dummy_image_dir, 'dummy.jpg')

        if not os.path.exists(dummy_image_path):
            img = Image.new('RGB', (100, 100), color = (128, 128, 128))
            img.save(dummy_image_path)
            self.stdout.write(self.style.SUCCESS(f'Created dummy image at "{dummy_image_path}"'))
        
        return dummy_image_path