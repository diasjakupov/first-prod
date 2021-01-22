from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


def book_poster(instance, filename):
    return f'book/poster/{instance.title}/{filename}'

def page(instance, filename):
    return f'book/pages/{instance.chapter.title}-{filename}'

class Category(models.Model):
    title=models.CharField(max_length=400, verbose_name="Название")

    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"

    def __str__(self):
        return self.title

class Genre(models.Model):
    title=models.CharField(max_length=400, verbose_name="Название")

    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"

    def __str__(self):
        return self.title

class Types(models.Model):
    title=models.CharField(max_length=400, verbose_name="Название")

    class Meta:
        verbose_name="Тип"
        verbose_name_plural="Типы"

    def __str__(self):
        return self.title




class Book(models.Model):
    STATUS=(
        ('end', 'end'),
        ('continue','continue')
    )

    likes=models.ManyToManyField(get_user_model(), blank=True, verbose_name='Лайки', related_name='books_like')
    title=models.TextField(verbose_name='Название')
    description=models.TextField(verbose_name='Описание')
    category=models.ManyToManyField(Category, verbose_name="Категория")
    genre=models.ManyToManyField(Genre, verbose_name="Жанр")
    types=models.ForeignKey(Types, on_delete=models.PROTECT, verbose_name="Тип", null=True, blank=True)
    views=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    created_date=models.PositiveIntegerField(null=True, blank=True, verbose_name='Дата добавление')
    status=models.TextField(choices=STATUS, null=True, blank=True, verbose_name="Статус")
    poster=models.ImageField(upload_to=book_poster, verbose_name='Главная картинка')
    average_rating=models.PositiveIntegerField(default=0, verbose_name='Рейтинг', validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.title


    def get_average_rating(self):
        value = 0
        count = self.rating.count()
        for i in self.rating.all():
            value += i.star.value
        if count == 0:
            count = 1
        return value//count

    class Meta:
        verbose_name='Манхва или Манга'
        verbose_name_plural='Манхва или Манга'


class Chapter(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapter',verbose_name='Манга или манхва')
    chapter_num=models.CharField(max_length=500,verbose_name='Номер главы (пример: Глава 1)', null=True, blank=True)
    title=models.CharField(max_length=500, verbose_name='Название главы')
    url=models.URLField(verbose_name='Ссылка на главу', null=True, blank=True)
    created_date=models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name='Глава'
        verbose_name_plural='Главы'

    def __str__(self):
        return self.title




class Page(models.Model):
    chapter=models.ForeignKey(Chapter, on_delete=models.CASCADE,verbose_name='Глава', related_name='page')
    picture=models.ImageField(upload_to=page, verbose_name='Страница', null=True)
    class Meta:
        verbose_name='Страница'
        verbose_name_plural='Страницы'

    def __str__(self):
        return f'{self.chapter.title}'



class RatingStars(models.Model):
    value = models.IntegerField(null=True)

    def __str__(self):
        value = str(self.value)
        return value

    class Meta:
        verbose_name='Звезды для рейтинга'
        verbose_name_plural='Звезды для рейтинга'


class Rating(models.Model):
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text=models.TextField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='rating')

    class Meta:
        verbose_name='Рейтинг'
        verbose_name_plural='Рейтинг'

    def __str__(self):
        star = str(self.star)
        return star