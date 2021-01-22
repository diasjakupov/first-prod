from django.urls import path, include
from.views import (
    BookViewSet, CreateRatingView, 
    PageViewSet, ChapterList, 
    AllListChapters, TypesList,
    GenreList, CategoryList,
    BookList, DetailBookview, getReviewsById,ChapterWPList)


urlpatterns = [
    path('', BookViewSet.as_view({'get':'list'})), 
    path('<int:pk>', DetailBookview.as_view()),
    path('filtered', BookList.as_view()),
    path('set_rating', CreateRatingView.as_view()),
    path('chapters', AllListChapters.as_view({'get':'list'})),
    path('types', TypesList.as_view()),
    path('genre', GenreList.as_view()),
    path('category', CategoryList.as_view()),
    path('chapter/<int:pk>', PageViewSet.as_view({'get': 'retrieve'})),
    path('book-detail-c/<int:pk>', ChapterList.as_view()),
    path('book-review/<int:pk>', getReviewsById.as_view()),
    path('chapter-wp/<int:pk>', ChapterWPList.as_view())
]