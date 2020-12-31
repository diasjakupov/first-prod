from django.urls import path, include
from .views import PublicUserViewset

urlpatterns = [
    path('<int:pk>', PublicUserViewset.as_view({'get':'retrieve'})),
    
]