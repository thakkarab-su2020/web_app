
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, OrderItem, Order, BookImage
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django import template
from django.core.exceptions import ObjectDoesNotExist
from .forms import BookForm, ImageForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from statsd import StatsClient
metric = StatsClient()

posts = 'This is a basic signin signup web application'


def about(request):
    context = {'posts': posts, 'title': 'About Us page'}

    return render(request, 'ui/about.html', context)


def home(request):
    context = {'books': Book.objects.all()}
    return render(request, 'ui/home.html', context)


# def delete_image(request):
#     image= Image.objects.get().delete()
#     return HttpResponseRedirect(reverse(""))
# safkjbe

class BookListView(ListView):

    model = Book
    template_name = 'ui/home.html'
    context_object_name = 'books'
    ordering = ['title', 'price']


class BookDetailView(DetailView):

    model = Book
    template_name = 'ui/book_detail.html'


# class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
# ....model = Book
# ....form_class=BookForm
# ....template_name = 'ui/book_form.html'
# ....success_message = "Book has been Added!"

# ....def form_valid(self, form):
# ........form.instance.seller = self.request.user
# ........return super().form_valid(form)

def post(request):

    ImageFormSet = modelformset_factory(BookImage, form=ImageForm,
            extra=3)

    if request.method == 'POST':

        bookForm = BookForm(request.POST)

        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=BookImage.objects.none())

        if bookForm.is_valid() and formset.is_valid():
            book_form = bookForm.save(commit=False)
            book_form.seller = request.user
            book_form.save()
            timer = metric.timer('create book')
            timer.start()
            for form in formset.cleaned_data:
                image = form['image']
                photo = BookImage(book=book_form, image=image)
                photo.save()
            messages.success(request, 'Posted!')
            logger.info('user added a product')
            metric.incr('books')
            timer.stop()
            return HttpResponseRedirect('/')
        else:
            print (bookForm.errors, formset.errors)
    else:
        bookForm = BookForm()
        formset = ImageFormSet(queryset=BookImage.objects.none())
    return render(request, 'ui/book_form.html', {'bookForm': bookForm,
                  'formset': formset})


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin,
    SuccessMessageMixin, UpdateView):

    model = Book
    fields = [
        'isbn',
        'title',
        'authors',
        'publication_date',
        'quantity',
        'price',
        ]
    template_name = 'ui/book_form.html'
    success_message = 'Book has been updated!'

    def test_func(self):
        book = self.get_object()
        timer = metric.timer('update book')
        timer.start()
        logger.info('user updated the book')
        if self.request.user == book.seller:
            timer.stop()
            return True

        return False


class AddImage(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    form_class = ImageForm
    model = BookImage
    template_name = 'ui/image_add.html'
    success_message = 'Image has been Added!'
    success_url = '/'

    def form_valid(self, form):
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        logger.info('user added the image')
        timer = metric.timer('add image')
        timer.start()
        BookImage = form.save()
        BookImage.save()
        timer.stop()
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin,
    DeleteView):

    model = Book
    template_name = 'ui/product_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        book = self.get_object()
        logger.info('user deleted the book')
        timer = metric.timer('delete book')
        timer.start()
        if self.request.user == book.seller:
            timer.stop()
            return True
        return False


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin,
    DeleteView):

    model = BookImage
    template_name = 'ui/image_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        bookimage = self.get_object()
        timer = metric.timer('delete image')
        timer.start()
        logger.info('user deleted the image')
        timer.stop()
        return True


@login_required
def update_cart(request, pk):
    item = get_object_or_404(Book, id=pk)
    (order_item, created) = OrderItem.objects.get_or_create(item=item,
            user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.pk).exists():
            if item.quantity == 0:
                messages.info(request, 'No more books to add')
                return redirect('product-summary')
            order_item.quantity += 1
            order_item.save()
            item.quantity -= 1
            item.save()
            messages.info(request, 'Product added to the cart')
            return redirect('product-summary')
        else:
            order.items.add(order_item)
            item.quantity -= 1
            item.save()
            messages.info(request, 'Product added to the cart')
            return redirect('book-detail', pk=pk)
    else:

        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                ordered_date=ordered_date)
        order_items.add(order_item)
        item.quantity -= 1
        item.save()
        messages.info(request, 'Product has been added to the cart')
        logger.info('user added a product to the cart')
        metric.incr('cart')
        return redirect('product-summary')


def delete_from_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item,
                    user=request.user, ordered=False)[0]
            item.quantity += order_item.quantity
            item.save()
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Product removed from the cart')
            logger.info('user deleted the product from the cart')
            metric.incr('cart')
            return redirect('product-summary')
        else:
            messages.info(request, 'Product is not in the cart')
            return redirect('book-detail', pk=pk)
    else:
        messages.info(request, 'No Orders')
        return redirect('book-detail', pk=pk)


def delete_single_item(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item,
                    user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.quantity += 1
                item.save()
                messages.info(request, 'Product removed from the cart')
                logger.info('user deleted the product from the cart')
                return redirect('product-summary')
            else:

                order.items.remove(order_item)
                messages.info(request, 'Product removed from the cart')
                item.quantity += 1
                item.save()
                return redirect('product-summary')
        else:
            messages.info(request, 'The item is not in the cart')
            return redirect('product-summary')
    else:
        messages.info(request, 'The item is not in the cart')
        return redirect('product-summary')


register = template.Library()


@register.filter
def item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


class ProductSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,
                    ordered=False)
            context = {'object': order}
            return render(self.request, 'ui/product_summary.html',
                          context)
        except ObjectDoesNotExist:
            messages.warning(self.request,
                             'You do not have an active order')
            return redirect('/')
