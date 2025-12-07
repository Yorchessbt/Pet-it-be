from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Solicitud
from .forms import AddPets, CommentForm, RequestForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden

# Create your views here.

def home(request):
    pets = Pet.objects.filter(status=Pet.EN_ADOPCION)[:3]
    context = {
        'pets': pets
    }
    return render(request, 'pets/index.html', context)

def adopt_me(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    related_pets = Pet.objects.filter(especie=pet.especie, status=Pet.EN_ADOPCION).exclude(pk=pk)[0:3]
    
    ya_solicito = Solicitud.objects.filter(pet=pet,perfil=request.user.perfil).exists()

    if request.method=='POST':
        formcoment = CommentForm(request.POST)
        if formcoment.is_valid():
            comment = formcoment.save(commit=False)
            comment.user = request.user
            comment.pet = pet
            comment.save()

            return redirect('adopt_me', pk=pk)
    else:
        formcoment = CommentForm()

    context = {
        'pet': pet,
        'related_pets': related_pets,
        'formcomment': formcoment,
        'ya_solicito': ya_solicito
    }

    return render(request, 'pets/pet.html', context)

def informacion(request):
    context = {

    }
    return render(request, 'pets/informacion.html', context)

def pets(request):
    
    pets = Pet.objects.all()
    tipo = request.GET.get('tipo', 'todos')

    if tipo != 'todos':
        try:
            pets = pets.filter(especie__tipo=int(tipo))
        except ValueError:
            pass
        
    context = {
        'pets': pets,
        'tipo': tipo
    }
    return render(request, 'pets/mascotas.html', context)


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = AddPets(request.POST, request.FILES)

        if form.is_valid():
            addpet = form.save(commit=False)
            addpet.creado_por = request.user
            addpet.slug = slugify(addpet.name)
            addpet.save()
            
            return redirect('adopt_me', pk=addpet.id)
    else:
        form= AddPets()

    context = {
        'form': form
    }

    return render(request, 'pets/add_pet.html', context)


@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method=='POST':
        petform = AddPets(request.POST, request.FILES, instance=pet)
        if petform.is_valid():
            petform.save()
            return redirect('adopt_me', pk=pet.id)
    else:
        petform = AddPets(instance=pet)
    context = {
        'pet': pet,
        'petform': petform,
    }
    return render(request, 'pets/edit_pet.html', context)


def search(request):
    query = request.GET.get('query', '')

    pets = Pet.objects.filter(status=Pet.EN_ADOPCION).filter(Q(name__icontains = query) | Q(especie__slug__icontains=query) )

    context = {
        'query':query,
        'pets': pets
    }
    return render(request, 'pets/search.html', context)

@login_required
def bandeja(request):
    perfil = request.user.perfil

    solicitudes = Solicitud.objects.filter(pet__creado_por=request.user).order_by('-fecha')

    context= {
        'solicitudes': solicitudes
    }

    return render(request, 'pets/bandeja.html', context)


@login_required
def solicitudes(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    ya_existe = Solicitud.objects.filter(
        pet=pet,
        perfil=request.user.perfil
    ).exists()

    if ya_existe:
        return HttpResponseForbidden("Ya mandaste una solicitud!!!")

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            soli = form.save(commit=False)
            soli.pet = pet
            soli.perfil = request.user.perfil
            soli.publicador = pet.creado_por.perfil
            soli.save()

            return redirect('bandeja_respuesta')
    else:
        form = RequestForm()
    
    context = {
        'form': form,
        'pet': pet
    }

    return render(request, 'pets/solicitudes.html', context)

@login_required
def bandeja_respuesta(request):
    perfil = request.user.perfil

    solicitudes = Solicitud.objects.filter(perfil=perfil).order_by('-fecha')

    context = {
        'solicitudes': solicitudes
        }
    
    return render(request, 'pets/respuestas.html', context)

@login_required
def respuesta(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)

    if solicitud.pet.creado_por != request.user:
        return HttpResponseForbidden("No eres el usuario de este post")

    accion = request.POST.get('accion')

    if accion == 'aceptar':
        solicitud.estado_solicitud = Solicitud.ACEPTADA
        solicitud.pet.status = Pet.ADOPTADO
        solicitud.pet.save()
        solicitud.save()

    elif accion == 'rechazar':
        solicitud.estado_solicitud = Solicitud.RECHAZADA
        solicitud.pet.save()
        solicitud.save()

    return redirect('bandeja')