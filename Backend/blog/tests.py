"""Test user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from blog.models import BlogContentImage # Added import

LOGIN_URL = reverse("user:login")
BLOG_CREATE = reverse("blog:create")
BLOG_IMAGE_UPLOAD_URL = reverse("blog:image-manage")

def create_user(**params):
    return get_user_model().objects.create_user(**params)

# Create your tests here.
class UserApiTests(TestCase):
    def setUp(self):
        paylaod = {
            "email": "test@example.com",
            "password": "testpass123",
            "username": "testuser",
            "name": "Test Name",
        }
        self.user = create_user(**paylaod)
        self.client = APIClient()

        res = self.client.post(LOGIN_URL, paylaod)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {res.data["access"]}')


    def test_create_blog_api(self):
        payload = {
            "name":'test blog',
            "content":"this is a test blog",
        }

        res = self.client.post(BLOG_CREATE , payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blog_content_image_api(self):
        """Test uploading an image for blog content"""
        image_name = "test_image.jpg"
        image_file = io.BytesIO()
        Image.new('RGB', (100, 100)).save(image_file, 'jpeg')
        image_file.seek(0)
        
        payload = {
            "name": "My Test Image",
            "image": SimpleUploadedFile(image_name, image_file.read(), content_type="image/jpeg")
        }

        res = self.client.post(
            BLOG_IMAGE_UPLOAD_URL,
            payload,
            format='multipart'
        )
        
        print(res.get('payload'))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image_url', res.data)

        image_obj = BlogContentImage.objects.get(name="My Test Image")

        image_obj.image.delete(save=False)
        image_obj.delete()