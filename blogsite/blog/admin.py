from django.contrib import admin
from .models import Post, Category, Tag, PostImage, Comment, Image


class PostImageInline(admin.TabularInline):
    """
    Allows adding and managing post images directly inside the Post admin page.
    """
    model = PostImage
    extra = 1
    
    readonly_fields = ['image_url']
    fields = ['image', 'position', 'image_url']
    def image_url(self, obj):
        if obj.image and obj.image.file:
            return obj.image.file.url
        return "-"
    


class CommentInline(admin.TabularInline):
    """
    Shows comments related to a post inside the Post admin page.
    """
    model = Comment
    extra = 0
    fields = ['name', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Blog Posts.
    """
    list_display = ['title', 'status', 'created_at', 'publish_at', 'views', 'likes']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostImageInline, CommentInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Blog Categories.
    """
    list_display = ['title', 'parent', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Blog Tags.
    """
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing and approving Comments.
    """
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'post__title']
    actions = ['approve_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        """
        Custom action to quickly approve multiple comments at once.
        """
        queryset.update(is_approved=True)
        
        



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    این کلاس مدل Image را به صورت مستقل به پنل ادمین معرفی می‌کند
    """
    list_display = ['id', 'file', 'alt_text', 'created_at']
    search_fields = ['alt_text']