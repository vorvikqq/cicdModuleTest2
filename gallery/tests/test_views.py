import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from gallery.models import Category, Image
from datetime import date
from django.urls import reverse
from django.test import Client


@pytest.fixture
def category_with_images(db):
    category = Category.objects.create(name="Sea")

    image1 = Image.objects.create(
        title="Black Sea",
        image=SimpleUploadedFile("image1.jpg", b"content", content_type="image/jpeg"),
        created_date=date.today(),
        age_limit=18
    )
    image2 = Image.objects.create(
        title="River View",
        image=SimpleUploadedFile("image2.jpg", b"content", content_type="image/jpeg"),
        created_date=date.today(),
        age_limit=12
    )

    image1.categories.add(category)
    image2.categories.add(category)

    return category, [image1, image2]
