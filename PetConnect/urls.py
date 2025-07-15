from django.contrib import admin
from django.urls import path
from PetConnect import views
import usuario.views
import tutores.views
import pets.views
import servicos.views
import atendimentos.views
import veterinarios.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login, name='login'),
    path('home/', views.Home, name='home'),
    path('autenticar/', usuario.views.login_view, name='autenticar'),
    path('sair/', usuario.views.logout_view, name='sair'),
    path('tutores/', views.Tutores, name='tutores'),
    path('tutores_form/', tutores.views.formulario_tutor, name='tutores_form'),
    path('tutores_del/', tutores.views.delete_tutor, name='tutores_del'),
    path('pets/', views.Pets, name='pets'),
    path('pets_form/', pets.views.formulario_pets, name='pets_form'),
    path('pets_del/', pets.views.delete_pet, name='pets_del'),
    path('atendimentos/', views.Atendimentos, name='atendimentos'),
    path('form_atendimento_del/', atendimentos.views.formulario_atendimento, name='form_atendimento'),
    path('form_atendimento_del/', atendimentos.views.formulario_atendimento, name='form_atendimento_del'),
    path('servicos/', views.Servico, name='servico'),
    path('formulario_servico/', servicos.views.formulario_servico, name='formulario_servico'),
    path('formulario_servico_del/', servicos.views.formulario_servico, name='formulario_servico_del'),
    path('veterinarios/', views.Veterinario, name='veterinarios'),
    path('veterinarios_form/', veterinarios.views.formulario_veterinarios, name='veterinarios_form'),
    path('veterinarios_del/', veterinarios.views.formulario_veterinarios, name='veterinarios_del'),
    path('financeiro/', views.Financeiro, name='financeiro'),
]
