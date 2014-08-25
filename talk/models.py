from django.db import models

class Sentence(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    input_text = models.TextField()
    output_text = models.TextField()
