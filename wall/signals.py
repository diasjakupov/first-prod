from django.db.models.signals import post_save, post_delete, pre_delete
from .models import Book, Chapter, Page, Rating
from django.dispatch import receiver
from PIL import Image

from .pp.parser import Parser
import requests
import os

path=os.path.dirname(os.path.abspath('media'))

def download_page(chapter_name, link, count):
    request=requests.get(link)
    content=request.content
    p_path=os.path.join(f'{path}\media\\book\pages', f'{chapter_name.book.title}-{chapter_name.title}-страница-{count}.jpeg')
    
    with open(p_path, 'wb') as file:
        file.write(content)

    return p_path

@receiver(post_save, sender=Book)
def change_size_of_poster(sender, instance, created, **kwargs):
    url=instance.poster
    img=Image.open(url.path)
    new_img=img.resize((300, 429))
    
    new_img.save(url.path)

@receiver(post_delete, sender=Book)
def delete_poster(sender, instance, **kwargs):
    os.remove(instance.poster.path)

@receiver(post_save, sender=Chapter)
def pars_pages(sender, instance, created, **kwargs):
    if created and instance.url is not None:
        url=instance.url
        p=Parser()
        data = p.start(url, True)
        count=1
        for index, data_list in enumerate(data):
            p_path=download_page(instance, data_list, count)
            idx=p_path.find(f'\\book\\')
            count +=1
            page=Page.objects.create(chapter=instance, picture=p_path)
            


@receiver(post_delete, sender=Page)
def delete_pages(sender, instance, **kwargs):
    print(instance.picture.path)
    os.remove(instance.picture.path)

@receiver(post_save, sender=Rating)
def save_av_rating(sender, instance, created, **kwargs):
    book=instance.book
    book.average_rating=book.get_average_rating()
    book.save()




