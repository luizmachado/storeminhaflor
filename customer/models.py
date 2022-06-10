from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(
        max_length=11, help_text='Insira o cpf sem pontuação', verbose_name='CPF')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # TODO: Override clean function to validate CPF
    def clean(self):
        pass

    class Meta():
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class CustomerAddress(models.Model):
    user = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, verbose_name='Usuário')
    address_title = models.CharField(
        max_length=10, verbose_name='Título Endereço')
    address = models.CharField(max_length=50, verbose_name='Endereço')
    number = models.CharField(max_length=5, verbose_name='Número')
    complement = models.CharField(max_length=30, verbose_name='Complemento')
    district = models.CharField(max_length=30, verbose_name='Bairro')
    cep = models.CharField(max_length=8, verbose_name='CEP')
    city = models.CharField(max_length=30, verbose_name='Cidade')
    estate = models.CharField(
        max_length=2,
        default='TO',
        verbose_name='Estado',
        choices=(('AC', 'Acre'),
                 ('AL', 'Alagoas'),
                 ('AP', 'Amapá'),
                 ('AM', 'Amazonas'),
                 ('BA', 'Bahia'),
                 ('CE', 'Ceará'),
                 ('DF', 'Distrito Federal'),
                 ('ES', 'Espírito Santo'),
                 ('GO', 'Goiás'),
                 ('MA', 'Maranhão'),
                 ('MT', 'Mato Grosso'),
                 ('MS', 'Mato Grosso do Sul'),
                 ('MG', 'Minas Gerais'),
                 ('PA', 'Pará'),
                 ('PB', 'Paraíba'),
                 ('PR', 'Paraná'),
                 ('PE', 'Pernambuco'),
                 ('PI', 'Piauí'),
                 ('RJ', 'Rio de Janeiro'),
                 ('RN', 'Rio Grande do Norte'),
                 ('RS', 'Rio Grande do Sul'),
                 ('RO', 'Rondônia'),
                 ('RR', 'Roraima'),
                 ('SC', 'Santa Catarina'),
                 ('SP', 'São Paulo'),
                 ('SE', 'Sergipe'),
                 ('TO', 'Tocantins'),))

    def __str__(self):
        return self.address_title

    # TODO: Override clean function to validate CEP
    def clean(self):
        pass

    class Meta():
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
