from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Collaborator
from django.utils import timezone
from django.contrib import messages


def home(request):
    team = Collaborator.objects.all()
    now = timezone.now()
    birthdays_today = team.filter(birth_date__day=now.day, birth_date__month=now.month)
    birthdays_count = birthdays_today.count()
    return render(request, "index.html", {"team": team, "birthdays_today": birthdays_today, "birthdays_count": birthdays_count})


def save(request):
    Collaborator_name = request.POST.get("colaborator_name")
    Collaborator_birth_date = request.POST.get("colaborator_birth_date")
    Collaborator_cpf = request.POST.get("colaborator_cpf")

    if Collaborator_cpf is None:
        messages.error(request, "CPF é obrigatório.")
        return redirect('home')

    if Collaborator.objects.filter(cpf=Collaborator_cpf).exists():
        messages.error(request, "Este CPF já existe!")
    else:
        try:
            Collaborator.objects.create(name=Collaborator_name, birth_date=Collaborator_birth_date, cpf=Collaborator_cpf)
            messages.success(request, "Colaborador salvo com sucesso!")
        except IntegrityError:
            messages.error(request, "Um colaborador com este nome já existe.")
        except ValueError:
            messages.error(request, "CPF inválido.")

    return redirect('home')  # Redireciona para a view home




def detail(request, id):
    collaborator = Collaborator.objects.get(id=id)
    return render(request, "update.html", {"collaborator": collaborator})


def update(request, id):
    collaborator_name = request.POST.get("collaborator_name")
    collaborator_birth_date = request.POST.get("collaborator_birth_date")
    collaborator_cpf = request.POST.get("collaborator_cpf")

    if not (collaborator_name and collaborator_birth_date and collaborator_cpf):
        messages.error(request, "Todos os campos são obrigatórios.")
        return redirect('home')

    collaborator = Collaborator.objects.get(id=id)
    collaborator.name = collaborator_name
    collaborator.birth_date = collaborator_birth_date
    collaborator.cpf = collaborator_cpf

    try:
        collaborator.save()
        messages.success(request, "Colaborador atualizado com sucesso!")
    except IntegrityError:
        messages.error(request, "Erro ao atualizar colaborador.")
    except ValueError:
        messages.error(request, "CPF inválido.")

    return redirect('home')


def delete(request, id):
    collaborator = Collaborator.objects.get(id=id)
    collaborator.delete()
    messages.success(request, "Colaborador deletado com sucesso!")
    return redirect('home')
