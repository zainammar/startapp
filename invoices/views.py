from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Invoice
from .forms import InvoiceForm


def invoice_list(request):
    search = request.GET.get('search', '')

    invoices = Invoice.objects.select_related(
        'customer',
        'created_by'
    ).all().order_by('-id')

    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) |
            Q(customer__customer_name__icontains=search)
        )

    paginator = Paginator(invoices, 10)
    page = request.GET.get('page')
    invoices = paginator.get_page(page)

    context = {
        'invoices': invoices,
        'search': search,
    }

    return render(request, 'invoices/invoice_list.html', context)


def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()

            messages.success(request, "Invoice created successfully.")
            return redirect("invoice_list")

    else:
        form = InvoiceForm()

    return render(request, "invoices/invoice_form.html", {
        "form": form,
        "title": "Create Invoice"
    })


def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related(
            'customer',
            'created_by'
        ),
        pk=pk
    )

    return render(request, "invoices/invoice_detail.html", {
        "invoice": invoice
    })


def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)

        if form.is_valid():
            form.save()

            messages.success(request, "Invoice updated successfully.")
            return redirect("invoice_list")

    else:
        form = InvoiceForm(instance=invoice)

    return render(request, "invoices/invoice_form.html", {
        "form": form,
        "title": "Edit Invoice"
    })


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == "POST":
        invoice.delete()

        messages.success(request, "Invoice deleted successfully.")
        return redirect("invoice_list")

    return render(request, "invoices/invoice_confirm_delete.html", {
        "invoice": invoice
    })