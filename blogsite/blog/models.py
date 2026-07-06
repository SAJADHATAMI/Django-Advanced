import os
from io import BytesIO

from ckeditor.fields import RichTextField
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image as PIL_Image
from django.contrib.auth import get_user_model
User = get_user_model()




class Status(models.TextChoices):
    """
    Status choices for blog posts.
    """

    draft = "draft", "Draft"
    review = "review", "Review"
    rejected = "rejected", "Rejected"
    published = "published", "Published"
    archived = "archived", "Archived"


class Post(models.Model):
    """
    Main model for blog posts.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="blogs/featured_images/%Y/%m")
    summary = RichTextField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(null=True, blank=True)

    images = models.ManyToManyField("Image", through="PostImage", related_name="posts")
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.draft
    )
    category = models.ManyToManyField("Category")
    tag = models.ManyToManyField("Tag", related_name="posts", blank=True)
    views = models.PositiveIntegerField(default=0, db_index=True)
    likes = models.PositiveIntegerField(default=0, db_index=True)
    dislikes = models.PositiveIntegerField(default=0, db_index=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["-publish_at", "-created_at"]

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Categories for grouping blog posts. Supports nested categories.
    """

    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "Category",
        related_name="cat_child",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Tags for flexible post classification.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    """
    Intermediary model to connect Posts and Images with a specific display position.
    """

    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="post_images"
    )
    image = models.ForeignKey(
        "Image", on_delete=models.CASCADE, related_name="post_images"
    )
    position = models.PositiveIntegerField(default=0, db_index=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(fields=["post", "image"], name="unique_post_image")
        ]

    def get_inner_url(self):
        """
        Returns the absolute URL of the optimized WebP image.
        """
        if self.image and self.image.file:
            return self.image.file.url
        return ""

    def get_html_tag(self):
        """
        Generates a complete HTML img tag with SEO alt text and a responsive class.
        """
        if self.image and self.image.file:
            alt = self.image.alt_text or self.post.title
            return f'<img src="{self.image.file.url}" alt="{alt}" class="responsive-blog-img" />'
        return ""


class Image(models.Model):
    """
    Standalone image model that automatically resizes and converts uploads to WebP.
    """

    file = models.ImageField(upload_to="blog/images/%Y/%m")
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Process image only when it is created for the first time
        if not self.pk:
            self.file.seek(0)
            img = PIL_Image.open(self.file)
            img = img.convert("RGB")

            # Resize image to maximum 1200x1200px maintaining aspect ratio
            img.thumbnail((1200, 1200))

            # Compress and convert image to WebP format
            buffered = BytesIO()
            img.save(buffered, format="WEBP", quality=70, optimize=True)

            # Extract the original filename without its old extension
            file_name, file_extension = os.path.splitext(self.file.name)

            # Create a new filename with .webp extension
            new_file_name = f"{file_name}.webp"

            # Save the new file content into the field without triggering a loop
            self.file.save(new_file_name, ContentFile(buffered.getvalue()), save=False)

        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Comments model for posts, supporting nested replies.
    """

    name = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "Comment",
        related_name="replies",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
