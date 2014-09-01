from django.contrib import admin
from talk.models import Sentence


class SentenceAdmin(admin.ModelAdmin):
    list_display = ('created', 'input_text', 'output_text')
    fields = ('input_text',)
admin.site.register(Sentence, SentenceAdmin)
