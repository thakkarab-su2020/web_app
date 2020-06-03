
from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView,ProductSummaryView
from . import views 

urlpatterns = [
    path('', BookListView.as_view(), name='ui-home'),
    path('about/',views.about, name='ui-about'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/new/', BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('book/cart/', ProductSummaryView.as_view(), name='product-summary'),
    path('update-cart/<int:pk>/', views.update_cart, name='update-cart'),
    path('delete-cart/<int:pk>/', views.delete_from_cart, name='delete-cart'),
    path('delete-item/<int:pk>/', views.delete_single_item, name='delete-item'),


]
