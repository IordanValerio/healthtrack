from django.shortcuts import render, redirect
from .models import BMIRecord
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    return render(request, "healthtrack/home.html")

#LOGIN

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "healthtrack/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "healthtrack/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "healthtrack/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "healthtrack/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "healthtrack/register.html")

#Minha view para a página de calculo do IMC
def bmi(request):

    imc = None
    categoria = None
    altura = None
    peso = None
    mensagem_sucesso = None

    if request.method == "POST":

        print(request.POST)

        acao = request.POST["acao"]

        if acao == "calcular":

            altura = float(request.POST["altura"])
            peso = float(request.POST["peso"])

            altura_metros = altura / 100
            imc = peso / (altura_metros ** 2)

            if imc < 18.5:
                categoria = "Underweight"
            elif imc < 25:
                categoria = "Normal weight"
            elif imc < 30:
                categoria = "Overweight"
            else:
                categoria = "Obesity"

        
        elif acao == "salvar":

            if not request.user.is_authenticated:
                historico = BMIRecord.objects.none()

                return render(request, "healthtrack/bmi.html", {
                    "erro_login": True,
                    "imc": None,
                    "historico": historico,
                    "categoria": None,
                    "altura": request.POST.get("altura", ""),
                    "peso": request.POST.get("peso", ""),
                })

            altura = float(request.POST["altura"])
            peso = float(request.POST["peso"])

            altura_metros = altura / 100
            imc = peso / (altura_metros ** 2)

            BMIRecord.objects.create(
                user=request.user,
                height=altura,
                weight=peso,
                bmi=imc,
            )
            mensagem_sucesso = "IMC salvo! Consulte o histórico abaixo."
    # O restante do código de salvar continua aqui

    # Busca todos os registros salvos no banco
    historico = BMIRecord.objects.all().order_by("-created_at")

    return render(request, "healthtrack/bmi.html", {
        "imc": round(imc, 2) if imc else None,
        "historico": historico,
        "categoria": categoria if imc else None,
        "altura": round(altura) if altura else "",
        "peso": round(peso, 2) if peso else "",
        "mensagem_sucesso": mensagem_sucesso,
    })

#Página sobre nutrição e alimentação saudável
def nutricao(request):
    return render(request, "healthtrack/nutrition.html")

def exercises(request):
    return render(request, "healthtrack/exercises.html")
