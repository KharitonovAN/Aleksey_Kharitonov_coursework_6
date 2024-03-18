from django.db import models

NULLABLE = {'null': True, 'blank': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blogpost/', verbose_name='Изображение', **NULLABLE)
    count_views = models.SmallIntegerField(default=0, verbose_name='Количество просмотров')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='В публикации')

    def __str__(self):
        return f'{self.title}/{self.count_views}/{self.date_published}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
