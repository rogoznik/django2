from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from .forms import ShopUserEditForm, ShopUserCreateForm
from .forms import ProductCategoryEditForm, ProductCategoryCreateForm
from .forms import ProductCreateForm, ProductEditForm


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return HttpResponseRedirect(reverse('adminapp:categories'))


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserCreateForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи/создание'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_edit.html'
    form_class = ShopUserEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи/редактирование'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return HttpResponseRedirect(reverse_lazy('adminapp:user_update', kwargs={'pk': user.pk}))


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи/удаление'
        return context


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryCreateForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории/создание'
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_edit.html'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории/редактирование'
        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        return HttpResponseRedirect(reverse_lazy('adminapp:category_update', kwargs={'pk': category.pk}))


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории/удаление'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.cat_pk = self.kwargs['pk']
        self.queryset = Product.objects.filter(category__pk=self.cat_pk).order_by('name')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукт'
        context['category'] = ProductCategory.objects.get(pk=self.cat_pk)
        context['objects'] = Product.objects.filter(category__pk=self.cat_pk).order_by('name')
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_create.html'
    form_class = ProductCreateForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты/создание'
        context['category_pk'] = self.cat_pk
        return context

    def get(self, request, *args, **kwargs):
        self.cat_pk = self.kwargs['pk']
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_product = form.save(commit=False)
        new_product.category_id = self.kwargs['pk']
        new_product.save()

        return HttpResponseRedirect(reverse_lazy('adminapp:products', kwargs={'pk': self.kwargs['pk']}))


def product_read(request, pk):
    pass


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_edit.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты/редактирование'
        context['category_id'] = self.cat_pk
        return context

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        self.cat_pk = product.category_id
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return HttpResponseRedirect(reverse_lazy('adminapp:product_update', kwargs={'pk': product.pk}))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_delete'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты/удаление'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(reverse_lazy('adminapp:products', kwargs={'pk': self.object.category_id}))
