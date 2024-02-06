from django.shortcuts import render, redirect
from .models import Registro, HistorialCambios
from django.contrib import messages
from django.db.models import Q
from .forms import FiltroRegistrosForm
from decimal import Decimal



# Create your views here.

def home(request):
    registros = Registro.objects.all()
    # messages.success(request, 'Listado de Registro de adquisiciones')
    return render(request, "gestionRegistros.html", {"registros": registros})

def registrarAdquisicion(request):
    Presupuesto = Decimal(request.POST['txtPresupuesto'])
    Unidad = request.POST['txtUnidad']
    Tipo = request.POST['txtTipo']
    Cantidad = Decimal(request.POST['txtCantidad'])
    ValorUnitario = Decimal(request.POST['txtValorUnitario'])
    FechaAdquisicion = request.POST['txtFecha']
    Proveedor = request.POST['txtProveedor']
    Documentacion = request.POST['txtDocumentacion']

    # Validar si el ValorTotal es mayor que el Presupuesto
    cantidad_decimal = Decimal(Cantidad)
    valor_unitario_decimal = Decimal(ValorUnitario)
    presupuesto_decimal = Decimal(Presupuesto)
    valor_total_nuevo = cantidad_decimal * valor_unitario_decimal

    if valor_total_nuevo > presupuesto_decimal:
        messages.error(request, 'El Valor Total (Cantidad * Valor Unitario) no puede ser mayor que el Presupuesto.')
        return redirect('/')

    registro = Registro.objects.create(
        Presupuesto=Presupuesto, 
        Unidad=Unidad, 
        Tipo=Tipo, 
        Cantidad=Cantidad, 
        ValorUnitario=ValorUnitario,
        FechaAdquisicion=FechaAdquisicion,
        Proveedor=Proveedor,
        Documentacion=Documentacion
    )

    

    return redirect('/')

def editarRegistro(request, idRegistro):
    registro = Registro.objects.get(idRegistro=idRegistro)

    # Obtener el historial completo de cambios para este registro
    historial_cambios = HistorialCambios.objects.filter(registro=registro).order_by('fecha_modificacion')

    # Crear un diccionario para almacenar los cambios agrupados por fecha
    cambios_agrupados = {}
    
    for cambio in historial_cambios:
        fecha_modificacion = cambio.fecha_modificacion.date()  # Extraer solo la fecha, sin la hora
        if fecha_modificacion not in cambios_agrupados:
            cambios_agrupados[fecha_modificacion] = []
        cambios_agrupados[fecha_modificacion].append(cambio)

    return render(request, 'editarRegistro.html', {'registro': registro, 'cambios_agrupados': cambios_agrupados})

def ver_registro(request, idRegistro):
    registro = Registro.objects.get(idRegistro=idRegistro)

    # Obtener todos los cambios para el registro
    historial_cambios = HistorialCambios.objects.filter(registro=registro).order_by('fecha_modificacion')

    # Crear un diccionario para almacenar los cambios agrupados por fecha
    cambios_agrupados = {}
    
    for cambio in historial_cambios:
        fecha_modificacion = cambio.fecha_modificacion.date()  # Extraer solo la fecha, sin la hora
        if fecha_modificacion not in cambios_agrupados:
            cambios_agrupados[fecha_modificacion] = []
        cambios_agrupados[fecha_modificacion].append(cambio)

    return render(request, 'verRegistro.html', {'registro': registro, 'cambios_agrupados': cambios_agrupados})



def editarAdquisicion(request):
    idRegistro = request.POST['txtid']
    Presupuesto = request.POST['txtPresupuesto']
    Unidad = request.POST['txtUnidad']
    Tipo = request.POST['txtTipo']
    Cantidad = request.POST['txtCantidad']
    ValorUnitario = request.POST['txtValorUnitario']
    FechaAdquisicion = request.POST['txtFecha']
    Proveedor = request.POST['txtProveedor']
    Documentacion = request.POST['txtDocumentacion']

    registro = Registro.objects.get(idRegistro=idRegistro)

    # Lista para almacenar los cambios
    cambios_realizados = []

    for campo in ['Presupuesto', 'Unidad', 'Tipo', 'Cantidad', 'ValorUnitario', 'FechaAdquisicion', 'Proveedor', 'Documentacion']:
        valor_anterior = getattr(registro, campo)
        nuevo_valor = request.POST.get(f'txt{campo}')

        # Guardar en el historial solo si hay un cambio
        if nuevo_valor is not None and valor_anterior != nuevo_valor:
            historial_cambio = HistorialCambios(
                registro=registro,
                campo_modificado=campo,
                valor_anterior=valor_anterior,
                nuevo_valor=nuevo_valor
            )
            historial_cambio.save()

            # Agregar el cambio a la lista
            cambios_realizados.append(historial_cambio)

    # Actualizar el registro con los nuevos valores
    registro.Presupuesto = Presupuesto
    registro.Unidad = Unidad
    registro.Tipo = Tipo
    registro.Cantidad = Cantidad
    registro.ValorUnitario = ValorUnitario
    registro.FechaAdquisicion = FechaAdquisicion
    registro.Proveedor = Proveedor
    registro.Documentacion = Documentacion
    registro.save()

    # Obtener la lista actualizada de registros
    registros = Registro.objects.all()

    # Renderizar la página principal con los registros actualizados
    return render(request, 'gestionRegistros.html', {'registros': registros})



def eliminarRegistro(request, idRegistro):
    registro = Registro.objects.get(idRegistro=idRegistro)
    registro.delete()

    return redirect('/')


def lista_registros(request):
    form = FiltroRegistrosForm(request.GET)
    registros = Registro.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('q')
        tipo_servicio = form.cleaned_data.get('tipo_servicio')
        valor_total_min = form.cleaned_data.get('valor_total_min')
        valor_total_max = form.cleaned_data.get('valor_total_max')
        fecha_adquisicion = form.cleaned_data.get('fecha_adquisicion')
        proveedor = form.cleaned_data.get('proveedor')

        # Filtrar en todos los campos del modelo
        if query:
            registros = registros.filter(
                Q(Tipo__icontains=query) |
                Q(Cantidad__icontains=query) |
                Q(ValorUnitario__icontains=query) |
                Q(ValorTotal__icontains=query) |
                Q(FechaAdquisicion__icontains=query) |
                Q(Proveedor__icontains=query) |
                Q(Documentacion__icontains=query)
            )

        if tipo_servicio is not None:
            registros = registros.filter(Tipo__icontains=tipo_servicio)

        if proveedor is not None:
            registros = registros.filter(Proveedor__icontains=proveedor)

        if valor_total_min is not None:
            registros = registros.filter(ValorTotal__gte=valor_total_min)

        if valor_total_max is not None:
            registros = registros.filter(ValorTotal__lte=valor_total_max)

        if fecha_adquisicion is not None:
            registros = registros.filter(FechaAdquisicion=fecha_adquisicion)

    return render(request, 'gestionRegistros.html', {'registros': registros, 'form': form})
