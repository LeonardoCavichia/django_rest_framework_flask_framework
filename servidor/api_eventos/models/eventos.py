from django.contrib.auth.models import User
from django.db import models

class Pessoa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, blank=False, null=False)
    email = models.CharField(max_length=250, blank=False, null=False)
    birthdate = models.DateTimeField(blank=False, null=False)
    status = models.SmallIntegerField(default=1)
    sex = models.CharField(max_length=1, blank=False, null=False)
    password = models.CharField(max_length=20,blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.username

class EventoTipo(models.Model):
    name = models.CharField(max_length=50)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Eventos(models.Model):
    title = models.CharField(max_length=250)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    street = models.CharField(max_length=250)
    neighborhood = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    referencePoint = models.CharField(max_length=250)
    description = models.TextField()
    status = models.BooleanField(default=True)
    eventType = models.ForeignKey(EventoTipo, on_delete=models.CASCADE)
    user = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.title

class PessoaEvento(models.Model):
    registrationDate = models.DateTimeField()
    eventoId = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    userId = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    objects = models.Manager()


class Mensagem(models.Model):
    participantId = models.ForeignKey(PessoaEvento, null=False, blank=False, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    messageDate = models.DateTimeField()
    objects = models.Manager()
    eventoId = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.message
