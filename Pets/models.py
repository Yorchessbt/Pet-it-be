from django.db import models
from django.contrib.auth.models import User
from Perfil.models import Perfil
# Create your models here.

tipo_animales = [
    [0, "Perro"],
    [1, "Gato"],
    [2, "Hamster"],
    [3, "Conejo"],
    [4, "Pajaro"],
    [5, "Tortuga"],
]

class Especie(models.Model):
    tipo = models.IntegerField(choices=tipo_animales)
    slug = models.SlugField()

    class Meta:
        ordering = ('tipo',)
        verbose_name_plural = 'razas'
    
    def __str__(self):
        return self.get_tipo_display()
    
    def get_absolute_url(self):
        return '/%s/' % self.slug

class Pet(models.Model):

    ADOPTADO = 'adoptado'
    EN_ADOPCION = 'en_adopcion'

    STATUS = {
        (ADOPTADO, 'Adoptado'),
        (EN_ADOPCION, 'En adopcion')
    }

    especie = models.ForeignKey(Especie, related_name='pets' , on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    descripcion = models.TextField()
    image = models.ImageField(upload_to='mascotas', blank=True, null=True)
    edad = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default=EN_ADOPCION)
    creado_por = models.ForeignKey(User, related_name='pets' , on_delete=models.CASCADE)
    public = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Comentario(models.Model):
    pet = models.ForeignKey(Pet, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username    

class Solicitud(models.Model):
    pet = models.ForeignKey(Pet, related_name='solicitudes', on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, related_name='solicitudes_enviadas', on_delete=models.CASCADE)
    publicador = models.ForeignKey(Perfil, related_name='solicitudes_recibidas', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    telefono = models.CharField(max_length=20)
    ocupacion = models.CharField(max_length=100)

    ESTADO_CIVIL = [
        ('soltero', 'Soltero(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viudo', 'Viudo(a)'),
        ('separado', 'Separado(a)')
    ]

    PENDIENTE = 'pendiente'
    ACEPTADA = 'aceptada'
    RECHAZADA = 'rechazada'

    ESTADOS_SOLICITUD = (
        (PENDIENTE, 'Pendiente'),
        (ACEPTADA, 'Aceptada'),
        (RECHAZADA, 'Rechazada'),
    )

    estado_solicitud = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default=PENDIENTE)
    estado = models.CharField(max_length=20, choices=ESTADO_CIVIL)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('pet', 'perfil')

    def __str__(self):
        return f"Solicitud para la mascota {self.pet.name} por parte de {self.perfil.user.username}" 