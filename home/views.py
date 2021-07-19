from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # admin paneldagi user modeli
from django.contrib import messages
from django.db import IntegrityError  # Pythonda mavjud bo'lmagan xatolik
# authenticate->signin qismini tekshiradi
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from .models import Home, mainBase, Qarz, InputQarz, PayAgent
from .forms import Basee, QarzForm, InputQarzForm, HomeForm, PayAgentForm, LendDebt
from datetime import date, datetime, timedelta
import json

admins = ['aslamjon', 'qobiljon']
agentsList = ['test']


def checkIsAdmin(request, html, sendObjToAdmin, sendObjToAnonimUser):
    if request.user.username in admins:
        sendObjToAdmin['isAdmin'] = True
        return render(request, html, sendObjToAdmin)
    else:
        if request.user.username in agentsList:
            sendObjToAnonimUser['isAgent'] = True
            return render(request, html, sendObjToAnonimUser)
        sendObjToAnonimUser['isAdmin'] = False
        return render(request, html, sendObjToAnonimUser)


def home(request):
    getHome = Home.objects.all()
    if (request.method == 'GET'):
        sentObjToTemplate = {'home': getHome, 'homeForm': HomeForm}

        return checkIsAdmin(request, 'html/index.html', sentObjToTemplate, sentObjToTemplate)
    elif (request.method == 'POST'):
        createBlogToHome = HomeForm(request.POST, request.FILES)
        if createBlogToHome.is_valid():
            createBlogToHome.save()
        # getHome
        # id yordamida home dagi cardlarni o'zgartirish kerak
        return redirect('home')


def editHome(request, home_id):
    product = get_object_or_404(Home, pk=home_id)
    if request.method == "GET":
        form = HomeForm(instance=product)
        sentToHomeEdit = {
            'form': form,
            'product': product
        }
        return checkIsAdmin(request, 'html/editHome.html', sentToHomeEdit, sentToHomeEdit)
    if (request.method == 'POST'):
        form = HomeForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        return redirect('home')


def deleteHome(request, home_id):
    blog = get_object_or_404(Home, pk=home_id)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')


def signup_user(request):
    if request.method == 'GET':
        user = UserCreationForm()  # signup
        return render(request, 'html/signUp.html', {'user': user})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # redirect render dan farqi unga funksiyalarni kiritsa bo'ladi.
                return redirect('home')
            except IntegrityError:
                return render(request, 'html/signUp.html', {'user': UserCreationForm(), 'error': 'Username sizdan oldin band qilngan'})

        else:
            return render(request, 'html/signUp.html', {'user': UserCreationForm(), 'error': 'Sizning parolingiz bir xil emas'})


def login_user(request):
    if request.method == 'GET':
        user = AuthenticationForm()
        return render(request, 'html/login.html', {'user': user})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'html/login.html', {'user': AuthenticationForm(), 'error': "username yoki parol xato iltimos qytadan urunib ko'ring"})
        else:
            login(request, user)
            return redirect('home')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# @login_required
#  ************ Baza ******************


def base(request):
    if (request.method == 'GET'):
        getBase = mainBase.objects.all()

        def getTotalRes(first):
            totalRes = {
                "priceSum": 0,
                "kgSum": 0,
                "debtSum": 0,
                "expectedBenefit": 0,
                "pratsent": 0
            }
            for i in range(len(first)):
                totalRes['priceSum'] += (first[i].kg * first[i].outsidePrice)
                totalRes['kgSum'] += first[i].kg
                totalRes['debtSum'] += first[i].totalLend
                totalRes['expectedBenefit'] += ((first[i].kg * first[i].outsidePrice) -
                                                (first[i].kg * first[i].insidePrice))
                totalRes['pratsent'] += (first[i].kg * first[i].outsidePrice)
            return totalRes
        if request.GET.get('search'):
            sendSearch = getBase.filter(
                byWhom__startswith=request.GET.get('search'))
            return checkIsAdmin(request, 'html/baza.html',
                                {'who': sendSearch[0].byWhom, 'totalData': getTotalRes(sendSearch), 'base': Basee, 'getBase': sendSearch, 'is_admin': True}, {'is_admin': False})
        else:
            return checkIsAdmin(request, 'html/baza.html',
                                {'totalData': getTotalRes(getBase), 'base': Basee, 'getBase': getBase, 'is_admin': True}, {'is_admin': False})

    elif (request.method == 'POST'):
        saveData = Basee(request.POST)
        getAllData = mainBase.objects.all()

        searchR = getAllData.filter(insidePrice__iexact=int(request.POST.get(
            'insidePrice')), outsidePrice__iexact=int(request.POST.get('outsidePrice')), typeOfProduct__iexact=request.POST.get('typeOfProduct'), byWhom__iexact=request.POST.get('byWhom'))
        if len(searchR) == 1:
            # agar bazaba budagi odama qarzash boshaq
            if searchR[0].debt:
                # agar qarzba xarisudagi boshaq
                if request.POST.get('debt') == 'on':
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('insidePrice')))
                    searchR[0].qarzSum += (int(request.POST.get('kg'))
                                           * int(request.POST.get('insidePrice')))
                else:
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('insidePrice')))
                searchR[0].save()
            else:
                # agar qarzba xarisudagi boshaq
                if request.POST.get('debt') == 'on':
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('insidePrice')))
                    searchR[0].qarzSum += (int(request.POST.get('kg'))
                                           * int(request.POST.get('insidePrice')))
                    searchR[0].debt = True
                else:
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('insidePrice')))
                searchR[0].save()
            return redirect('base')
        else:
            saveData.save()
            getBase = mainBase.objects.all()
            searchRes = getBase[len(getBase)-1]
            if searchRes.debt and searchRes.qarzSum == 0:
                searchRes.qarzSum = searchRes.totalSum
                searchRes.save()
        return redirect('base')
    else:
        return render(request, 'html/404.html')


def editItem(request, product_id):
    product = get_object_or_404(mainBase, pk=product_id)
    if request.method == "GET":
        form = Basee(instance=product)
        sendToTemplate = {
            'product': product, 'form': form, 'LendDebt': LendDebt,
            'formId': product_id
        }
        return checkIsAdmin(request, 'html/edit.html', sendToTemplate, {"a": 'a'})
    elif request.method == "POST":
        if len(request.POST) < 4:
            form = LendDebt(request.POST, instance=product)
            form2 = Basee(instance=product)
            sendToTemplate = {
                'product': product, 'form': form2, 'LendDebt': LendDebt,
                'error': '', 'formId': product_id
            }
            if form.is_valid():
                product.qarzSum -= int(request.POST.get('lastLendDebt'))
                product.totalLend += int(request.POST.get('lastLendDebt'))
                form.save()
                product.save()

                return redirect('base')
            else:
                sendToTemplate['error'] = "raqam yoki sana kiritmadingiz iltimos qaytadan urinib ko'ring"
                return checkIsAdmin(request, 'html/edit.html', sendToTemplate, {})

        else:
            form = Basee(request.POST, instance=product)
            if form.is_valid():
                form.save()
                product.changed = True
                product.save()
                return redirect('base')
    else:
        return redirect('base')


def deleteBase(request, product_id):
    blog = get_object_or_404(mainBase, pk=product_id)
    if request.method == 'POST':
        blog.delete()
        return redirect('base')
# ***************************************************

# this function get lastMonth


def prev_month(date=date.today()):
    if date.month == 1:
        return date.replace(month=12, year=date.year-1)
    else:
        try:
            return date.replace(month=date.month-1)
        except ValueError:
            return prev_month(date=date.replace(day=date.day-1))


def agentTake(request):
    getAgentsData = Qarz.objects.all()
    getInputQarz = InputQarz.objects.all()
    getPayAgent = PayAgent.objects.all()
    if request.method == 'GET':

        def getTotalRes(first, second):
            totalRes = {
                "priceSum": 0,
                "kgSum": 0,
                "debtSum": 0,
                "expectedBenefit": 0,
                "pratsent": 0
            }
            for i in range(len(first)):
                totalRes['priceSum'] += (first[i].kg * first[i].price)
                totalRes['kgSum'] += first[i].kg
                totalRes['debtSum'] += second[i].totalLend
                totalRes['expectedBenefit'] += ((first[i].kg * first[i].price) -
                                                (first[i].kg * first[i].orginalPrice))
                totalRes['pratsent'] += (first[i].kg * first[i].price)
            return totalRes
        if request.GET.get('search'):
            sendSearch = getAgentsData.filter(
                byWhom__startswith=request.GET.get('search'))
            sendSearch2 = getInputQarz.filter(
                byWhom__startswith=request.GET.get('search'))
            totalRes = getTotalRes(sendSearch, sendSearch2)
            # if checkbox on this it get data lastMonth
            if request.GET.get('checkbox') == 'on':
                sendSearch = sendSearch.filter(
                    afterCreateDate__gte=prev_month())
                sendSearch2 = sendSearch2.filter(
                    afterCreateDate__gte=prev_month())

            return checkIsAdmin(request, 'html/agentTake.html',
                                {'who': sendSearch[0].byWhom, 'payAgent': PayAgentForm, 'totalRes': totalRes, 'isAdmin': True, 'range': range(len(sendSearch)), 'getAgentsData': list(sendSearch), 'qarzForm': QarzForm, 'getInputQarz': sendSearch2}, {'isAdmin': False})
        else:
            totalRes = getTotalRes(getAgentsData, getInputQarz)
            return checkIsAdmin(request, 'html/agentTake.html', {'totalRes': totalRes, 'range': range(len(getAgentsData)), 'isAdmin': True, 'getAgentsData': list(getAgentsData), 'qarzForm': QarzForm, 'getInputQarz': getInputQarz}, {'isAdmin': False})
    elif request.method == 'POST':
        form = QarzForm(request.POST)
        form2 = InputQarz(byWhom=request.POST.get('byWhom'), qarzSum=0, oxirgiQarzBerganVaqti=date(
            1900, 1, 1), totalLend=0)
        if form.is_valid():
            form.save()
            form2.save()
            return redirect('agentTake')
        else:
            return checkIsAdmin(request, 'html/agentTake.html', {'range': range(len(getAgentsData)), 'isAdmin': True, 'getAgentsData': list(getAgentsData), 'qarzForm': QarzForm, 'getInputQarz': getInputQarz, 'error': "Xatolik mavjud iltimos qaytadan urunib ko'ring"}, {'isAdmin': False})


def editAgent(request, agent_id):
    agent = get_object_or_404(Qarz, pk=agent_id)
    agent2 = get_object_or_404(InputQarz, pk=agent_id)
    if request.method == "GET":
        form = QarzForm(instance=agent)
        form2 = InputQarzForm(instance=agent2)
        return render(request, 'html/editAgent.html', {'error': False, 'isAdmin': True, 'agent': agent, 'form': form, 'form2': form2, 'formId': agent_id, 'totalLend': agent2.totalLend})
    elif request.method == 'POST':
        form11 = QarzForm(instance=agent)
        form22 = InputQarzForm(instance=agent2)
        if len(request.POST) < 4:
            form = InputQarzForm(request.POST, instance=agent2)
            if form.is_valid():
                if agent.debt:
                    lend = int(request.POST['qarzSum'])
                    if lend <= agent.totalSum:
                        agent.totalSum -= lend
                        agent2.totalLend += lend
                        if agent.totalSum <= 0:
                            agent.debt = False
                        form.save()
                        agent.save()
                        agent2.save()
                        return redirect('agentTake')
                    else:
                        return render(request, 'html/editAgent.html', {'error': "Qarzidan ko'proq mablag'z kiritdingiz", 'isAdmin': True, 'agent': agent, 'form': form11, 'form2': form22, 'formId': agent_id, 'totalLend': agent2.totalLend})
                else:
                    return render(request, 'html/editAgent.html', {'error': "Qarz mavjud emas", 'isAdmin': True, 'agent': agent, 'form': form11, 'form2': form22, 'formId': agent_id, 'totalLend': agent2.totalLend})
        else:
            form = QarzForm(request.POST, instance=agent)
            if form.is_valid():
                form.save()
                agent.changed = True
                agent.save()
                return redirect('agentTake')


def delete(request, agent_id):
    blog = get_object_or_404(Qarz, pk=agent_id)
    blog2 = get_object_or_404(InputQarz, pk=agent_id)
    if request.method == 'POST':
        blog.delete()
        blog2.delete()
        return redirect('agentTake')


def payToAgent(request):
    if request.method == 'POST':
        getPayAgent = PayAgent.objects.all()

        scan = getPayAgent.filter(who__startswith=request.POST.get('who'))
        if len(scan) == 1:
            getId = scan[0].id
            blog = get_object_or_404(PayAgent, pk=getId)
            blog.payAgent += int(request.POST.get('payAgent'))
            blog.lastPayAgent = int(request.POST.get('payAgent'))
            blog.date = date.today()
            return redirect('agentTake')
        elif len(scan) == 0:
            form = PayAgentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('agentTake')
        else:
            return redirect('agentTake')
    elif request.method == 'GET':
        getData = PayAgent.objects.all()
        return checkIsAdmin(request, 'html/paidToAgent.html', {'getData': getData}, {})
    else:
        return redirect('agentTake')
