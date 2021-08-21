from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # admin paneldagi user modeli
from django.contrib import messages
from django.db import IntegrityError  # Pythonda mavjud bo'lmagan xatolik
# authenticate->signin qismini tekshiradi
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from .models import Home, mainBase, Qarz, PayAgent, Baza, Agents, Admins, TakeMoneyFromBazar
from .forms import Basee, QarzForm, InputQarzForm, HomeForm, PayAgentForm, LendDebt, BazaForm, LendDebtForBaza, AgentsForm, TakeMoneyFromBazarForm
from datetime import date, datetime, timedelta


admins = ['aslamjon', 'qobiljon']
agentsList = []


def checkIsAdmin(request, html, sendObjToAdmin, sendObjToAnonimUser):
    getAdmins = Admins.objects.all()
    global admins
    admins = []
    for i in getAdmins:
        admins.append(i.name)
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
    getAgents = Agents.objects.all()
    for i in getAgents:
        agentsList.append(i.name)
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
    else:
        sentObjToTemplate = {'home': getHome, 'homeForm': HomeForm}
        return checkIsAdmin(request, 'html/index.html', sentObjToTemplate, sentObjToTemplate)


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
def baza(request):
    def getDataFromBaza():
        return Baza.objects.all()
    def sendToTemplateForAdmin():
        return {
            'bazaForm': BazaForm,
            'getBaza': getDataFromBaza()
        }
    if (request.method == 'GET'):
        return checkIsAdmin(request, 'html/realBaza.html',sendToTemplateForAdmin(), {})
    elif request.method == 'POST':
        saveData = BazaForm(request.POST)
        if saveData.is_valid():
            saveData.save()
            getBase = getDataFromBaza()
            searchRes = getBase[len(getBase)-1]
            if searchRes.debt and searchRes.debtSum == 0:
                searchRes.debtSum = searchRes.totalSum
            searchRes.kgOrg = searchRes.kg
            searchRes.save()
            return redirect('baza')
        else:
            getData = sendToTemplateForAdmin()
            getData['error'] = "Ma'lumot kiritishda xotolik yuz berdi" 
            return checkIsAdmin(request, 'html/realBaza.html', getData, {})

def editBaza(request, get_id):
    product = get_object_or_404(Baza, pk=get_id)
    if request.method == "GET":
        form = BazaForm(instance=product)
        sendToTemplate = {
            'product': product, 'form': form, 'LendDebtForBaza': LendDebtForBaza,
            'formId': get_id
        }
        return checkIsAdmin(request, 'html/editRealBaza.html', sendToTemplate, {"a": 'a'})
    elif request.method == 'POST':
        if len(request.POST) < 4:
            form = LendDebtForBaza(request.POST, instance=product)
            
            sendToTemplate = {
                'product': product, 'LendDebt': LendDebtForBaza,
                'error': '', 'formId': get_id
            }
            if form.is_valid():
                product.debtSum -= int(request.POST.get('lastLendDebt'))
                product.totalLend += int(request.POST.get('lastLendDebt'))
                form.save()
                product.save()

                return redirect('baza')
            else:
                sendToTemplate['error'] = "Ma'lumot to'liq kiritilmagan qaydadan urinib ko'ring"
                return checkIsAdmin(request, 'html/editRealBaza.html', sendToTemplate, {"a": 'a'})
        else:
            if product.kg == product.kgOrg and not product.changed:
                product.kgOrg = float(request.POST.get('kg'))
            form = BazaForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                product.changed = True
                product.save()
                return redirect('baza')
    else:
        return redirect('baza')

def deleteBaza(request, get_id):
    product = get_object_or_404(Baza, pk=get_id)
    if request.method == 'POST':
        product.delete()
        return redirect('baza')

#  ************ Bozor ******************
def base(request):
    def getTotalRes(first,secound=0):
        totalRes = {
            "priceSum": 0,
            'rest':0,
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
        totalRes['priceSum'] = int(totalRes['priceSum'])
        totalRes['debtSum'] = int(totalRes['debtSum'])
        totalRes['expectedBenefit'] = int(totalRes['expectedBenefit'])
        totalRes['pratsent'] = int(totalRes['pratsent'])
        if not secound == 0:
            for item in secound:
                totalRes['rest'] += item.TakeMoney
            totalRes['rest'] = totalRes['priceSum'] - totalRes['rest']
        return totalRes
    if (request.method == 'GET'):
        getBase = mainBase.objects.all()
        getDataFromBaza = Baza.objects.all()
        if request.GET.get('search'):
            sendSearch = getBase.filter(
                byWhom__startswith=request.GET.get('search'))
            return checkIsAdmin(request, 'html/baza.html',
                                {'baza':getDataFromBaza ,'who': sendSearch[0].byWhom, 'totalData': getTotalRes(sendSearch, TakeMoneyFromBazar.objects.all()), 'base': Basee, 'getBase': sendSearch, 'is_admin': True}, {'is_admin': False})
        else:
            return checkIsAdmin(request, 'html/baza.html',
                                {'TakeMoneyFromBazarForm':TakeMoneyFromBazarForm,'baza':getDataFromBaza ,'totalData': getTotalRes(getBase, TakeMoneyFromBazar.objects.all()), 'base': Basee, 'getBase': getBase, 'is_admin': True}, {'is_admin': False})

    elif (request.method == 'POST'):
        saveData = Basee(request.POST)
        getAllData = mainBase.objects.all()

        getDataFromBaza = Baza.objects.all()
        filterBazaForFindingPrice = getDataFromBaza.filter(typeOfProduct__exact=request.POST.get('typeOfProduct'))
        changeKgOrg = Baza.objects.get(id=filterBazaForFindingPrice[0].id)
        searchR = getAllData.filter(
            outsidePrice__exact=int(request.POST.get('outsidePrice')), 
            typeOfProduct__exact=request.POST.get('typeOfProduct'), 
            byWhom__exact=request.POST.get('byWhom'))
        # bu haqida malumot bo'lsa ustiga qo'shadi
        if len(searchR) == 1:
            # agar bazaba budagi odama qarzash boshaq
            if searchR[0].debt:
                # agar qarzba xarisudagi boshaq
                if request.POST.get('debt') == 'on':
                    searchR[0].kg += float(request.POST.get('kg'))
                    searchR[0].totalSum += (float(request.POST.get('kg'))
                                            * int(request.POST.get('outsidePrice')))
                    searchR[0].qarzSum += (float(request.POST.get('kg'))
                                           * int(request.POST.get('outsidePrice')))
                else:
                    searchR[0].kg += float(request.POST.get('kg'))
                    searchR[0].totalSum += (float(request.POST.get('kg'))
                                            * int(request.POST.get('outsidePrice')))
                searchR[0].save()
            else:
                # agar qarzba xarisudagi boshaq
                if request.POST.get('debt') == 'on':
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('outsidePrice')))
                    searchR[0].qarzSum += (int(request.POST.get('kg'))
                                           * int(request.POST.get('outsidePrice')))
                    searchR[0].debt = True
                else:
                    searchR[0].kg += int(request.POST.get('kg'))
                    searchR[0].totalSum += (int(request.POST.get('kg'))
                                            * int(request.POST.get('outsidePrice')))
                searchR[0].save()
            changeKgOrg.kgOrg -= float(request.POST.get('kg'))
            changeKgOrg.save()
            return redirect('base')
        else:
            # oldin bu haqida malumot bo'lmasa yaratadi
            getBase = mainBase.objects.all()
            if saveData.is_valid():
                if (changeKgOrg.kgOrg - float(request.POST.get('kg'))) >= 0:
                    saveData.save()
                    changeKgOrg.kgOrg -= float(request.POST.get('kg'))
                    changeKgOrg.save()
                    # agar qarzga olgan bo'lsa
                    searchRes = getBase[len(getBase)-1]
                    if searchRes.debt and searchRes.qarzSum == 0:
                        searchRes.qarzSum = searchRes.totalSum
                    
                    searchRes.insidePrice = filterBazaForFindingPrice[0].price
                    searchRes.save()
                else:
                    return checkIsAdmin(request, 'html/baza.html',
                                {"error":"Bazada yetarli yuk mavjud emas. Iltimos tekshirib qaytadan kiritishga harakat qiling.",'baza':getDataFromBaza ,'totalData': getTotalRes(getBase), 'base': Basee, 'getBase': getBase, 'is_admin': True}, {'is_admin': False})
            else:
                return checkIsAdmin(request, 'html/baza.html',
                                {"error":"Ma'lumot kiritayotganda xotolik bo'ldi. Iltimos qaytadan urinib ko'ring",'baza':getDataFromBaza ,'totalData': getTotalRes(getBase), 'base': Basee, 'getBase': getBase, 'is_admin': True}, {'is_admin': False})
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
            getDataFromBaza = Baza.objects.all()
            filterBazaForFindingPrice = getDataFromBaza.filter(typeOfProduct=request.POST.get('typeOfProduct'))
            changeKgOrg = Baza.objects.get(id=filterBazaForFindingPrice[0].id)
            if product.kg > float(request.POST.get('kg')):
                temp = product.kg - float(request.POST.get('kg'))
                changeKgOrg.kgOrg += temp
            elif product.kg < float(request.POST.get('kg')):
                temp = float(request.POST.get('kg')) - product.kg
                changeKgOrg.kgOrg -= temp
            if not product.typeOfProduct == request.POST.get('typeOfProduct'):
                product.insidePrice = filterBazaForFindingPrice[0].price
                filterBazaOldKgOfProduct = Baza.objects.get(typeOfProduct=product.typeOfProduct)
                filterBazaOldKgOfProduct.kgOrg += float(product.kg)
                filterBazaOldKgOfProduct.save()
                changeKgOrg.kgOrg -= float(request.POST.get('kg'))
            form = Basee(request.POST, instance=product)
            if form.is_valid():
                form.save()
                product.changed = True
                product.save()
                changeKgOrg.save()
            return redirect('base')
    else:
        return redirect('base')


def deleteBase(request, product_id):
    blog = get_object_or_404(mainBase, pk=product_id)
    if request.method == 'POST':
        blog.delete()
        return redirect('base')
# *********************- TakeMoney -******************************
def addMoneyWhenTakeMoney(request):
    if request.method == "GET":
        content = {
            'TakeMoneyFromBazar': TakeMoneyFromBazar.objects.all(),
            'TakeMoneyFromBazarForm':TakeMoneyFromBazarForm,
        }
        return checkIsAdmin(request, 'html/whenTakeMoney.html', content, {})

    if request.method == "POST":
        form = TakeMoneyFromBazarForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('addMoneyWhenTakeMoney')

def deleteAddMoneyWhenTakeMoney(request, block_id):
    blog = get_object_or_404(TakeMoneyFromBazar, pk=block_id)
    if request.method == 'POST':
        blog.delete()
    return redirect('addMoneyWhenTakeMoney')
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
    # getInputQarz = InputQarz.objects.all()
    getPayAgent = PayAgent.objects.all()
    sendToTemplate = {
            'range': range(len(getAgentsData)), 
            'getAgentsData': list(getAgentsData), 
            'qarzForm': QarzForm, 
            'getInputQarz': getAgentsData
    }
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
        totalRes['priceSum'] = int(totalRes['priceSum'])
        totalRes['debtSum'] = int(totalRes['debtSum'])
        totalRes['expectedBenefit'] = int(totalRes['expectedBenefit'])
        totalRes['pratsent'] = int(totalRes['pratsent'])
        return totalRes
    if request.method == 'GET':
        getDataFromBaza = Baza.objects.all()
        sendToTemplate['baza'] = getDataFromBaza
        
        if request.GET.get('search'):
            sendSearch = getAgentsData.filter(
                byWhom__startswith=request.GET.get('search'))
            totalRes = getTotalRes(sendSearch, sendSearch)
            # if checkbox on this it get data lastMonth
            if request.GET.get('checkbox') == 'on':
                sendSearch = sendSearch.filter(
                    afterCreateDate__gte=prev_month())
            sendToTemplate['who'] = sendSearch[0].byWhom
            sendToTemplate['payAgent'] = PayAgentForm
            sendToTemplate['totalRes'] = totalRes
            sendToTemplate['range'] = range(len(sendSearch))
            sendToTemplate['getAgentsData'] = list(sendSearch)
            sendToTemplate['getInputQarz'] = sendSearch
            return checkIsAdmin(request, 'html/agentTake.html', sendToTemplate, {'isAdmin': False})
        else:
            totalRes = getTotalRes(getAgentsData, getAgentsData)
            sendToTemplate['totalRes'] = totalRes
            return checkIsAdmin(request, 'html/agentTake.html', sendToTemplate, {'isAdmin': False})
    elif request.method == 'POST':
        form = QarzForm(request.POST)
        getDataFromBaza = Baza.objects.all()
        filterBaza = getDataFromBaza.filter(typeOfProduct__exact=request.POST.get('typeOfProduct'))
        changeKgOrg = Baza.objects.get(id=filterBaza[0].id)
        if form.is_valid():
            if (changeKgOrg.kgOrg - float(request.POST.get('kg'))) >= 0:
                changeKgOrg.kgOrg -= float(request.POST.get('kg'))
                form.save()
                changeKgOrg.save()
                getBase = Qarz.objects.all()
                if len(getBase) > 0:
                    searchRes = getBase[len(getBase)-1]
                    searchRes.orginalPrice = filterBaza[0].price
                    searchRes.save()
                return redirect('agentTake')
            else:
                totalRes = getTotalRes(getAgentsData, getAgentsData)
                sendToTemplate['totalRes'] = totalRes
                sendToTemplate['error'] = "Bazada buncha yuk mavjud emas. Iltimos tekshirib qaytadan harakat qilib ko'ring"
                return checkIsAdmin(request, 'html/agentTake.html', sendToTemplate, {'isAdmin': False})
        else:
            return checkIsAdmin(request, 'html/agentTake.html', {'range': range(len(getAgentsData)), 'getAgentsData': list(getAgentsData), 'qarzForm': QarzForm, 'getInputQarz': getAgentsData, 'error': "Xatolik mavjud iltimos qaytadan urunib ko'ring"}, {'isAdmin': False})
    else:
        return redirect('agentTake')

def editAgent(request, agent_id):
    agent = get_object_or_404(Qarz, pk=agent_id)
    # agent2 = get_object_or_404(InputQarz, pk=agent_id)
    if request.method == "GET":
        form = QarzForm(instance=agent)
        form2 = InputQarzForm(instance=agent)
        return render(request, 'html/editAgent.html', {'error': False, 'isAdmin': True, 'agent': agent, 'form': form, 'form2': form2, 'formId': agent_id, 'totalLend': agent.totalLend})
    elif request.method == 'POST':
        form11 = QarzForm(instance=agent)
        form22 = InputQarzForm(instance=agent)
        if len(request.POST) < 4:
            form = InputQarzForm(request.POST, instance=agent)
            if form.is_valid():
                if agent.debt:
                    lend = int(request.POST['qarzSum'])
                    if lend <= agent.totalSum:
                        agent.totalSum -= lend
                        agent.totalLend += lend
                        if agent.totalSum <= 0:
                            agent.debt = False
                        form.save()
                        agent.save()
                        return redirect('agentTake')
                    else:
                        return render(request, 'html/editAgent.html', {'error': "Qarzidan ko'proq mablag'z kiritdingiz", 'isAdmin': True, 'agent': agent, 'form': form11, 'form2': form22, 'formId': agent_id, 'totalLend': agent.totalLend})
                else:
                    return render(request, 'html/editAgent.html', {'error': "Qarz mavjud emas", 'isAdmin': True, 'agent': agent, 'form': form11, 'form2': form22, 'formId': agent_id, 'totalLend': agent.totalLend})
        else:
            getDataFromBaza = Baza.objects.all()
            filterBazaForFindingPrice = getDataFromBaza.filter(typeOfProduct=request.POST.get('typeOfProduct'))
            changeKgOrg = Baza.objects.get(id=filterBazaForFindingPrice[0].id)
            if agent.kg > int(request.POST.get('kg')):
                # hozir kiritayotgan kg oldingisidan kam bo'lsa
                temp = agent.kg - int(request.POST.get('kg'))
                changeKgOrg.kgOrg += temp
            elif agent.kg < int(request.POST.get('kg')):
                # hozir kiritayotgan kg oldingisidan ko'p bo'lsa
                temp = int(request.POST.get('kg')) - agent.kg
                changeKgOrg.kgOrg -= temp
            if not agent.typeOfProduct == request.POST.get('typeOfProduct'):
                agent.orginalPrice = filterBazaForFindingPrice[0].price
                filterBazaOldKgOfProduct = Baza.objects.get(typeOfProduct=agent.typeOfProduct)
                filterBazaOldKgOfProduct.kgOrg += int(agent.kg)
                filterBazaOldKgOfProduct.save()
                changeKgOrg.kgOrg -= int(request.POST.get('kg'))
            form = QarzForm(request.POST, instance=agent)
            if form.is_valid():
                form.save()
                agent.changed = True
                agent.save()
                changeKgOrg.save()
                return redirect('agentTake')


def delete(request, agent_id):
    blog = get_object_or_404(Qarz, pk=agent_id)
    # blog2 = get_object_or_404(InputQarz, pk=agent_id)
    if request.method == 'POST':
        blog.delete()
        # blog2.delete()
        return redirect('agentTake')

def addRealBazaWhenHaveProducts(request, product_id):
    product = get_object_or_404(Baza, pk=product_id)
    if request.method == 'POST':
        product.kgOrg += float(request.POST['addKg'])
        product.kg += float(request.POST['addKg'])
        product.save()
    return redirect('baza')


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

def addAgent(request):
    sendToTemplate = {
        'agentForm': AgentsForm,
        'agents': Agents.objects.all()
    }
    if request.method == 'GET':
        return checkIsAdmin(request, 'html/addAgent.html', sendToTemplate, {})
    elif request.method == 'POST':
        form = AgentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addAgent')
        else:
            return checkIsAdmin(request, 'html/addAgent.html', sendToTemplate, {})

def deleteAgent(request, deleteAgent_id):
    agent = get_object_or_404(Agents, pk=deleteAgent_id)
    if request.method == 'GET':
        agent.delete()
        return redirect('addAgent')


