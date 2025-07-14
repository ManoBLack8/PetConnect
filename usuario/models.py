from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50, blank=False)
    senha = models.CharField(max_length=50, blank=False)
    telefone = models.CharField(max_length=15, blank=True)
    dataCadastro = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome
