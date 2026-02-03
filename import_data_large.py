# djangoS3/gestion_taches/import_data_large.py

import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_taches.settings")
django.setup()

from taches.models import Intervenant, Client, Intervention

# --- إعداد بيانات المتدخلين ---
postes = ['Technicien', 'Ingénieur', 'Consultant', 'Chef de projet', 'Analyste']
prenoms_intervenant = ['Ahmed','Fatima','Ali','Zineb','Omar','Salim','Sara','Youssef','Lina','Mohamed',
                       'Amina','Khalid','Nadia','Hassan','Mariam','Rachid','Sami','Leila','Karim','Sana',
                       'Ilyas','Souad','Rania','Adil','Samira','Nabil','Imane','Bilal','Yara','Tarek',
                       'Nada','Amine','Selma','Rayan','Soufiane','Hiba','Walid','Lamia','Anas','Malak']

nom_intervenant = ['Benali','Trabelsi','Moussaoui','Ould','Khalifa','Haddad','Bensalem','Raimi','Cherif','Jalloul',
                   'Fadel','Mahmoud','Chouaib','Sahraoui','Toumi','Belkacem','Hassan','Amara','Yahia','Saidi',
                   'Naji','Karim','Bouta','Rami','Samir','Fathi','Meriem','Lotfi','Salma','Hakim',
                   'Imad','Nour','Rania','Amin','Dalia','Youssef','Safa','Marwa','Omar','Siham']

intervenants_data = []
for i in range(40):
    intervenants_data.append({
        'nom': nom_intervenant[i % len(nom_intervenant)],
        'prenom': prenoms_intervenant[i % len(prenoms_intervenant)],
        'poste': random.choice(postes)
    })

# --- إعداد بيانات العملاء ---
societes = ['Société A','Société B','Société C','Société D','Société E','Société F','Société G','Société H']
prenoms_client = ['Omar','Salim','Sara','Youssef','Lina','Mohamed','Amina','Khalid','Nadia','Hassan',
                  'Mariam','Rachid','Sami','Leila','Karim','Sana','Ilyas','Souad','Rania','Adil',
                  'Samira','Nabil','Imane','Bilal','Yara','Tarek','Nada','Amine','Selma','Rayan',
                  'Soufiane','Hiba','Walid','Lamia','Anas','Malak','Zainab','Youssef','Meriem','Rami']

clients_data = []
for i in range(40):
    clients_data.append({
        'nom': random.choice(societes),
        'prenom': prenoms_client[i % len(prenoms_client)]
    })

# --- إضافة المتدخلين ---
for i in intervenants_data:
    Intervenant.objects.get_or_create(**i)

# --- إضافة العملاء ---
for c in clients_data:
    Client.objects.get_or_create(**c)

# --- إضافة تدخلات عشوائية ---
types_intervention = ['Réparation', 'Installation', 'Maintenance', 'Audit', 'Formation']
etats_intervention = ['En cours','Terminée','Annulée']

intervenants = list(Intervenant.objects.all())
clients = list(Client.objects.all())

# لكل متدخل، إضافة تدخلات عشوائية (1 إلى 5 تدخلات لكل واحد)
for intervenant in intervenants:
    for _ in range(random.randint(1,5)):
        client = random.choice(clients)
        Intervention.objects.create(
            type=random.choice(types_intervention),
            date=date.today() - timedelta(days=random.randint(0,30)),  # تواريخ عشوائية خلال آخر 30 يوم
            intervenant=intervenant,
            client=client,
            etat=random.choice(etats_intervention)
        )

print("✅ تم إضافة 40 متدخل و40 عميل وتدخلات عشوائية بنجاح!")
