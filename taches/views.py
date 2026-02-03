from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Intervenant, Client, Intervention
from .forms import IntervenantForm, ClientForm, InterventionForm

# Home
@login_required
def home(request):
    return render(request, 'taches/home.html')

# Auth
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'taches/login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect'})
    return render(request, 'taches/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Intervenants
@login_required
def intervenant_list(request):
    data = Intervenant.objects.all()
    return render(request, 'taches/intervenant_list.html', {'data': data})


@login_required
def intervenant_add(request):
    form = IntervenantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('intervenant_list')
    return render(request, 'taches/form.html', {'form': form})

@login_required
def intervenant_delete(request, pk):
    intervenant = get_object_or_404(Intervenant, pk=pk)
    intervenant.delete()
    return redirect('intervenant_list')

# Clients
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'taches/client_list.html', {'clients': clients})

@login_required
def client_add(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, 'taches/form.html', {'form': form})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('client_list')

# Interventions
@login_required
def intervention_list(request):
    interventions = Intervention.objects.all()
    return render(request, 'taches/intervention_list.html', {'interventions': interventions})

@login_required
def intervention_add(request):
    form = InterventionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('intervention_list')
    return render(request, 'taches/form.html', {'form': form})

@login_required
def intervention_delete(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    intervention.delete()
    return redirect('intervention_list')

# Stats
@login_required
def stats(request):
    # Placeholder pour statistiques
    return render(request, 'taches/stats.html')

from django.http import HttpResponse
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from .models import Intervention

@login_required
def stats_pdf(request):
    from .models import Intervention, Intervenant
    import matplotlib.pyplot as plt
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import ImageReader

    # --- بيانات المهام لكل intervenant ---
    intervenants = Intervenant.objects.all()
    noms = [i.nom for i in intervenants] if intervenants.exists() else ['Aucun']
    taches_realisees = [Intervention.objects.filter(intervenant=i).count() for i in intervenants] \
                       if intervenants.exists() else [0]

    fig1, ax1 = plt.subplots(figsize=(8,4))
    ax1.bar(noms, taches_realisees, color='skyblue')
    ax1.set_title("Tâches réalisées par chaque intervenant")
    ax1.set_ylabel("Nombre de tâches")
    ax1.set_xlabel("Intervenants")
    plt.xticks(rotation=45, ha='right')
    buf1 = io.BytesIO()
    fig1.tight_layout()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    plt.close(fig1)

    # --- بيانات توزيع المهام حسب الحالة ---
    etats = ['Réalisée', 'En attente']
    nb_taches = [Intervention.objects.filter(etat=etat).count() or 0 for etat in etats]

    # إذا كان كل شيء صفر لتجنب NaN
    if sum(nb_taches) == 0:
        nb_taches = [1, 0]

    fig2, ax2 = plt.subplots(figsize=(6,6))
    ax2.pie(nb_taches, labels=etats, autopct='%1.1f%%', startangle=90)
    ax2.set_title("Répartition des tâches selon l'état")
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    plt.close(fig2)

    # --- إنشاء PDF ---
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statistiques.pdf"'
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.drawImage(ImageReader(buf1), 50, height/2 + 50, width=500, height=250)
    c.drawImage(ImageReader(buf2), 50, 50, width=500, height=250)
    c.showPage()
    c.save()

    return response


