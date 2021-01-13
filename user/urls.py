from django.urls import path, include
from .views import PublicUserViewset, PrivateUserViewSet

urlpatterns = [
    path('<int:pk>', PublicUserViewset.as_view({'get':'retrieve'})),
    path('my_profile', PrivateUserViewSet.as_view())
]