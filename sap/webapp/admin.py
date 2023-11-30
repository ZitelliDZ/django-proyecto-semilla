from django.contrib import admin

# Register your models here.

from .models import Article, ArticleSeries
# Register your models here.

class ArticleSeriesAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'subtitle',
        'slug',
        'author',
        'image',
        #'published'
    ]
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header',{'fields':['title', 'subtitle','article_slug','series','author','image']}),
        ('Content',{'fields':['content','notes' ]}),
        ('Date',{'fields':['modified', ]})
        
        #'title' ,
        #'subtitle' ,
        #'article_slug', 
        #'content', 
        ##'published', 
        #'modified', 
        #'series' ,
    ]

admin.site.register(ArticleSeries, ArticleSeriesAdmin)
admin.site.register(Article, ArticleAdmin)