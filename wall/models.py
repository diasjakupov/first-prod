from django.db import models

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

    title=models.TextField(verbose_name='Название')
    description=models.TextField(verbose_name='Описание')
    category=models.ManyToManyField(Category, verbose_name="Категория")
    genre=models.ManyToManyField(Genre, verbose_name="Жанр")
    types=models.ForeignKey(Types, on_delete=models.PROTECT, verbose_name="Тип", null=True, blank=True)
    views=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    created_date=models.PositiveIntegerField(null=True, blank=True, verbose_name='Дата добавление')
    status=models.TextField(choices=STATUS, null=True, blank=True, verbose_name="Статус")
    poster=models.ImageField(upload_to=book_poster, verbose_name='Главаня картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Манхва или Манга'
        verbose_name_plural='Манхва или Манга'


class Chapter(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapter',verbose_name='Манга или манхва')
    title=models.CharField(max_length=500, verbose_name='Название главы')
    url=models.TextField(verbose_name='Ссылка на главу')
    created_date=models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name='Глава'
        verbose_name_plural='Главы'

    def __str__(self):
        return self.title


class Page(models.Model):
    picture=models.ImageField(upload_to=page, verbose_name='Страница')
    chapter=models.ForeignKey(Chapter, on_delete=models.CASCADE,verbose_name='Глава')

    class Meta:
        verbose_name='Страница'
        verbose_name_plural='Страницы'

    def __str__(self):
        return f'{self.chapter.title}'