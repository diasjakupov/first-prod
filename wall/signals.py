from django.db.models.signals import post_save, post_delete, pre_delete
from .models import Book, Chapter, Page
from django.dispatch import receiver

from .pp.parser import Parser
import requests
import os

path=os.path.abspath('media')

def download_page(chapter_name,link, count):
    request=requests.get(link)
    content=request.content
    p_path=os.path.join(f'{path}\\book\pages', f'{chapter_name}-{count}.jpeg')
    
    with open(p_path, 'wb') as file:
        file.write(content)

    return p_path



   

@receiver(post_save, sender=Chapter)
def pars_pages(sender, instance, created, **kwargs):
    if created and instance.url is not None:
        url=instance.url
        p=Parser()
        data = p.start(url, True)
        count=1
        for i in data:
            p_path=download_page(instance.title, i, count)
            count +=1
            Page.objects.create(chapter=instance, picture=p_path)


@receiver(post_delete, sender=Page)
def delete_pages(sender, instance, **kwargs):
    os.remove(f'{instance.picture}')




