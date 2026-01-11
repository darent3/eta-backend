from django.db import models
from django.conf import settings
from wagtail.search import index
import PyPDF2
import os

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    search_fields = [
        index.SearchField('title', partial_match=True, boost=2),
        index.SearchField('extracted_text', partial_match=True),
    ]

    def save(self, *args, **kwargs):
        # Save the file first so Django can set the proper file path
        super().save(*args, **kwargs)

        # Extract text from PDF if file is a PDF
        if self.file and self.file.name.endswith('.pdf') and not self.extracted_text:
            try:
                # Get full file path
                file_path = self.file.path
                print(f"DEBUG: Trying to open: {file_path}")
                print(f"DEBUG: File exists? {os.path.exists(file_path)}")

                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    self.extracted_text = text
                print(f"✓ Extracted {len(text)} characters")
                # Save again to update extracted_text
                super().save(update_fields=['extracted_text'])
            except Exception as e:
                print(f"✗ Error extracting PDF text: {e}")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    pdf_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, default='For the Curious')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Volunteer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ['-joined_at']


class Donation(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    stripe_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} from {self.email}"

    class Meta:
        ordering = ['-created_at']


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
