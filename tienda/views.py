
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto, Cliente
from .forms import CategoriaForm, ProductoForm, ClienteForm
from django.db.models import Count, Sum


# ---------- INICIO ----------
def inicio(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'categorias': categorias
    })


# ---------- CATEGORÍAS (CRUD) ----------
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categorias/lista.html', {
        'categorias': categorias
    })


@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'tienda/categorias/form.html', {
        'form': form,
        'titulo': 'Crear Categoría'
    })


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'tienda/categorias/form.html', {
        'form': form,
        'titulo': 'Editar Categoría'
    })


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('lista_categorias')

    return render(request, 'tienda/categorias/eliminar.html', {
        'categoria': categoria
    })


# ---------- PRODUCTOS (CRUD) ----------
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos/lista.html', {
        'productos': productos
    })


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'tienda/productos/form.html', {
        'form': form,
        'titulo': 'Crear Producto'
    })


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'tienda/productos/form.html', {
        'form': form,
        'titulo': 'Editar Producto'
    })


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_productos')

    return render(request, 'tienda/productos/eliminar.html', {
        'producto': producto
    })


# ---------- CLIENTES (CRUD) ----------
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'tienda/clientes/lista.html', {
        'clientes': clientes
    })


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'tienda/clientes/form.html', {
        'form': form,
        'titulo': 'Crear Cliente'
    })


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'tienda/clientes/form.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('lista_clientes')

    return render(request, 'tienda/clientes/eliminar.html', {
        'cliente': cliente
    })


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    total_categorias = Categoria.objects.count()
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()

    productos_activos = Producto.objects.filter(activo=True).count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()

    valor_inventario = Producto.objects.aggregate(
        total=Sum('precio')
    )['total'] or 0

    ultimos_productos = Producto.objects.order_by('-id')[:5]

    # Productos por categoría
    por_categoria = (
        Categoria.objects
        .annotate(num_productos=Count('producto'))
        .order_by('-num_productos')
    )

    context = {
        'total_categorias': total_categorias,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'productos_activos': productos_activos,
        'productos_sin_stock': productos_sin_stock,
        'valor_inventario': valor_inventario,
        'ultimos_productos': ultimos_productos,
        'por_categoria': por_categoria,
    }

    return render(request, 'tienda/dashboard.html', context)
