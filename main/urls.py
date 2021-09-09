from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('books', views.books),
    path('books/add', views.booksadd),
    path('books/<nom>', views.booksview),
    path('user/<nem>', views.userview),
    path('delete/<nim>', views.deletereview),
    path('addreview/<nam>', views.addreview)
]
