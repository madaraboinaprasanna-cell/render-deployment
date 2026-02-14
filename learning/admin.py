from django.contrib import admin
from .models import Topic, LearningPath, Resource, UserProgress

class ResourceInline(admin.TabularInline):
    model = Resource.learning_path.through
    extra = 1

class LearningPathAdmin(admin.ModelAdmin):
    filter_horizontal = ('topics',)
    # Resource is M2M via related_name='resources' on Resource model pointing to LearningPath on 'learning_path' field.
    # Wait, Resource has `learning_path = models.ManyToManyField(LearningPath, related_name='resources')`
    # So LearningPath has `resources` reversed.
    pass

admin.site.register(Topic)
admin.site.register(LearningPath, LearningPathAdmin)
admin.site.register(Resource)
admin.site.register(UserProgress)
