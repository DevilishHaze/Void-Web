from django.db import models
from django.contrib.auth.models import User
from backend.constellations.models import Constellation


class Articles(models.Model):
    constellation = models.OneToOneField(Constellation, on_delete=models.CASCADE,related_name='Созвездие', verbose_name='Cозвездие')
    title = models.CharField(max_length=200,verbose_name='Название Статьи')
    content = models.TextField(verbose_name="Контент")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Cтатьи'

    def __str__(self):
        return self.title

class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments',verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автори')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан ')
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return "Комментарий: {}".format(self.id)


class FavoriteArticle(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Избранная статья'
        verbose_name_plural = 'Избранные статьи'
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user} - {self.article.title}"
