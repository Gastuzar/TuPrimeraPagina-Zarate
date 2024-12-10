from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Plato, Mesa, Reserva
from restaurant.forms import PlatoForm, MesaForm, ReservaForm, BuscarPlatoForm, BuscarReservaForm

def menu(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = PlatoForm()

    buscar_form = BuscarPlatoForm(request.GET)
    platos = Plato.objects.all()

    if buscar_form.is_valid():
        nombre = buscar_form.cleaned_data.get('nombre')
        categoria = buscar_form.cleaned_data.get('categoria')

        if nombre:
            platos = platos.filter(nombre__icontains=nombre)
        if categoria:
            platos = platos.filter(categoria=categoria)

        if not platos.exists():
            buscar_form.add_error(None, "No se ha encontrado ese plato.")

    return render(
        request,
        'restaurant/menu.html',
        {'form': form, 'buscar_form': buscar_form, 'platos': platos}
    )


def mesas(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mesas')
    else:
        form = MesaForm()
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'restaurant/mesas.html', {'form': form, 'mesas': mesas})

def reservas(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservas')
    else:
        form = ReservaForm()
    buscar_form = BuscarReservaForm(request.GET)
    reservas = Reserva.objects.all().order_by('fecha', 'hora')
    mensaje = None 

    if buscar_form.is_valid():
        nombre_cliente = buscar_form.cleaned_data.get('nombre_cliente')
        fecha = buscar_form.cleaned_data.get('fecha')
        if nombre_cliente:
            reservas = reservas.filter(nombre_cliente__icontains=nombre_cliente)
        if fecha:
            reservas = reservas.filter(fecha=fecha)
        if not reservas.exists():
            mensaje = "No se encontró ninguna reserva con los criterios especificados."
            buscar_form.add_error(None, mensaje)
    
    return render(request, 'restaurant/reservas.html', {
        'form': form, 
        'buscar_form': buscar_form, 
        'reservas': reservas
    })

def base(request):
    bienvenida = "Bienvenido"
    return render(request, 'restaurant/base.html', {'bienvenida': bienvenida})

