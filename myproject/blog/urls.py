
from django.urls import path
from .views import BookListView, BookDetailView, BookUpdateView, BookDeleteView,ProductSummaryView , ImageDeleteView , AddImage
from . import views 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', BookListView.as_view(), name='ui-home'),
    path('about/',views.about, name='ui-about'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # path('book/new/', BookCreateView.as_view(), name='book-create'),
    path('book/new/', views.post, name='book-create'),
    path('books/<int:pk>/add-image/', AddImage.as_view(), name="add-image"),
    # path('deleteimage/', views.delete_image, name='delete-image'),
    path('book/<int:book>/deleteimage/<int:pk>', ImageDeleteView.as_view(), name='delete-image'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('book/cart/', ProductSummaryView.as_view(), name='product-summary'),
    path('update-cart/<int:pk>/', views.update_cart, name='update-cart'),
    path('delete-cart/<int:pk>/', views.delete_from_cart, name='delete-cart'),
    path('delete-item/<int:pk>/', views.delete_single_item, name='delete-item'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)