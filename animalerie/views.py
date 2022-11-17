from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnimalForm
from .models import Animal, Equipement
# Create your views here.
def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animaux': animaux, 'equipements': equipements})

def animal_detail(request, id_animal):
    animaux = Animal.objects.all()
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = Equipement.objects.get(id_equip=animal.lieu.id_equip)
    ancien = ancien_lieu.id_equip
    form = AnimalForm(request.POST, instance=animal)
    if form.is_valid():
        #Gestion du lieu
        nouveau_lieu = form.cleaned_data['lieu']
        nouveau = nouveau_lieu.id_equip
        #On détermine si le changement de lieu est valide
        if nouveau_lieu.disponibilite == "libre":
            if ancien == "litière":
                if nouveau == "mangeoire":
                    compatible = True
                else:
                    compatible = False
            elif ancien == "mangeoire":
                if nouveau == "roue":
                    compatible = True
                else:
                    compatible = False
            elif ancien == "roue":
                if nouveau == "nid":
                    compatible = True
                else:
                    compatible = False
            elif ancien == "nid":
                if nouveau == "litière":
                    compatible = True
                else:
                    compatible = False
        else:
            compatible = False
        #Si oui, on change de lieu
        if compatible:
            form.save()
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            if nouveau_lieu.id_equip != "litière":
                nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            #En on change d'état !
            if nouveau_lieu.id_equip == "litière":
                animal.etat = "affamé"
                animal.save()
            elif nouveau_lieu.id_equip == "mangeoire":
                animal.etat = "repus"
                animal.save()
            elif nouveau_lieu.id_equip == "roue":
                animal.etat = "épuisé"
                animal.save()
            elif nouveau_lieu.id_equip == "nid":
                animal.etat = "endormi"
                animal.save()
            context = {'animal': animal, 'nouveau_lieu': nouveau_lieu}
            return render(request, 'animalerie/success.html', context)
        else:
            context = {'animal': animal, 'nouveau_lieu': nouveau_lieu}
            return render(request, 'animalerie/fail.html', context)
    else:
        form = AnimalForm()
        context = {'animaux': animaux, 'animal': animal, 'form': form}
        return render(request, 'animalerie/animal_detail.html', context)

def rules(request):
    return render(request, "animalerie/rules.html")

