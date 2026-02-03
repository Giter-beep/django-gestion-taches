from django.db import models

class Intervenant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    poste = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    direction = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Intervention(models.Model):
    TYPE_CHOICES = [
        ('Soft', 'Soft'),
        ('Hard', 'Hard'),
    ]
    ETAT_CHOICES = [
        ('En attente', 'En attente'),
        ('Réalisée', 'Réalisée'),
    ]

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    motive = models.TextField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES)
    intervenant = models.ForeignKey(Intervenant, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} - {self.etat}"
