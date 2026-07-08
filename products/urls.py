from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product
from .forms import ProductForm


def product_list(request):
    search = request.GET.get('search', '')

    products = Product.objects.select_related('category').all()

    if search:
        products = products.filter(
            Q(product_name__icontains=search) |
            Q(product_code__icontains=search) |
            Q(barcode__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'search': search,
    }

    return render(request, 'products/product_list.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'products/product_detail.html', {
        'product': product
    })


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })