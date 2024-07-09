# Importando as bibliotecas necessárias
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Collaborator
from django.utils import timezone
from django.contrib import messages

# Função para exibir a página inicial
def home(request):
    team = Collaborator.objects.all()
    now = timezone.now()
    birthdays_today = team.filter(birth_date__day=now.day, birth_date__month=now.month)
    birthdays_count = birthdays_today.count()
    return render(request, "index.html", {"team": team, "birthdays_today": birthdays_today, "birthdays_count": birthdays_count})

# Função para salvar um novo colaborador
def save(request):
    Collaborator_name = request.POST.get("colaborator_name")
    Collaborator_birth_date = request.POST.get("colaborator_birth_date")
    Collaborator_cpf = request.POST.get("colaborator_cpf")

    if not (Collaborator_name and Collaborator_birth_date and Collaborator_cpf ):
        messages.error(request, "Todos os campos são obrigatórios.")
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

# Função para exibir detalhes de um colaborador
def detail(request, id):
    collaborator = Collaborator.objects.get(id=id)
    return render(request, "update.html", {"collaborator": collaborator})

# Função para atualizar um colaborador existente
def update(request, id):
    collaborator_name = request.POST.get("collaborator_name")
    collaborator_birth_date = request.POST.get("collaborator_birth_date")

    if not (collaborator_name and collaborator_birth_date):
        messages.error(request, "Todos os campos são obrigatórios.")
        return redirect('detail', id=id)  

    collaborator = Collaborator.objects.get(id=id)
    collaborator.name = collaborator_name
    collaborator.birth_date = collaborator_birth_date

    try:
        collaborator.save()
        messages.success(request, "Colaborador atualizado com sucesso!")
    except IntegrityError:
        messages.error(request, "Erro ao atualizar colaborador.")
    except ValueError:
        messages.error(request, "CPF inválido.")

    return redirect('home')

# Função para deletar um colaborador
def delete(request, id):
    collaborator = Collaborator.objects.get(id=id)
    collaborator.delete()
    messages.success(request, "Colaborador deletado com sucesso!")
    return redirect('home')
