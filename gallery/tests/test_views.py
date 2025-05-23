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


@pytest.mark.django_db
def test_gallery_view_no_categories(client):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert b'No categories' in response.content or len(response.context['categories']) == 0


@pytest.mark.django_db
def test_gallery_view_all_categories_and_images(client, category_with_images):
    category, images = category_with_images

    url = reverse('main')
    response = client.get(url)

    assert response.status_code == 200
    assert category.name in str(response.content)
    for image in images:
        assert image.title in str(response.content)


@pytest.mark.django_db
def test_image_detail_invalid_id_format(client):
    response = client.get('/image/abc/')
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("image_id, expected_status", [
    (1, 200),
    (999, 404)
])
def test_image_detail(client, image_id, expected_status):
    category = Category.objects.create(name="Animals")
    image = Image.objects.create(
        title="Lion",
        image=SimpleUploadedFile("lion.jpg", b"content", content_type="image/jpeg"),
        created_date=date.today(),
        age_limit=10
    )
    image.categories.add(category)

    url = reverse('image_detail', kwargs={'pk': image_id})
    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status == 200:
        assert image.title in str(response.content)