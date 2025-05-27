from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=25)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    search_time = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    def __str__(self):
        return f"{self.city.name} - {self.search_time}"
    
    class Meta:
        verbose_name = "История поиска"
        verbose_name_plural = "История поисков"
        ordering = ['-search_time']
