from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category
from .forms import CategoryForm


def category_list(request):
    search = request.GET.get('search', '')

    categories = Category.objects.all().order_by('category_name')

    if search:
        categories = categories.filter(
            Q(category_name__icontains=search)
        )

    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    context = {
        'categories': categories,
        'search': search,
    }

    return render(request, 'categories/category_list.html', context)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'categories/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'categories/category_detail.html', {
        'category': category
    })


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

    return render(request, 'categories/category_confirm_delete.html', {
        'category': category
    })