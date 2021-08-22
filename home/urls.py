from django.urls import path
from .views import home, signup_user, logout_user, login_user, base, editItem, agentTake, editAgent, delete, deleteHome, editHome, payToAgent, deleteBase, baza, editBaza, deleteBaza, addAgent, deleteAgent, addRealBazaWhenHaveProducts, addMoneyWhenTakeMoney, deleteAddMoneyWhenTakeMoney, returnProduct

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:home_id>', deleteHome, name='deleteHome'),
    path('<int:home_id>', editHome, name='editHome'),
    # Note Auth
    path('signup/', signup_user, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    # Note Baza
    path('baza/', baza, name='baza'),
    path('baza/<int:get_id>', editBaza, name='editBaza'),
    path('baza/delete/<int:get_id>', deleteBaza, name='deleteBaza'),
    path('baza/add/<int:product_id>', addRealBazaWhenHaveProducts, name='addRealBazaWhenHaveProducts'),
    # Note bozor
    path('bozor/', base, name='base'),
    path('bozor/addMoney', addMoneyWhenTakeMoney, name='addMoneyWhenTakeMoney'),
    path('bozor/addMoney/delete/<int:block_id>', deleteAddMoneyWhenTakeMoney, name='deleteAddMoneyWhenTakeMoney'),
    path('bozor/<int:product_id>', editItem, name='editItem'),
    path('bozor/delete/<int:product_id>', deleteBase, name='deleteBase'),
    path('bozor/return/<int:returnProduct_id>', returnProduct, name='returnProduct'),
    # Savdo tochkasi
    path('savdo/', agentTake, name='agentTake'),
    path('savdo/<int:agent_id>', editAgent, name='editAgent'),
    path('savdo/delete/<int:agent_id>', delete, name='delete'),
    path('savdo/payToAgent', payToAgent, name='payToAgent'),
    path('addAgent/', addAgent, name='addAgent'),
    path('addAgent/deleteAgent/<int:deleteAgent_id>', deleteAgent, name='deleteAgent'),
]