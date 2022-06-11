from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.documentos_utils import checar_validade, formata_documento, checar_cep, formata_cep


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(
        max_length=14, verbose_name='CPF')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # Override clean fuction do validate CPF
    def clean(self):
        error_messages = {}
        if len(self.cpf) == 14:
            if not checar_validade(self.cpf):
                error_messages['cpf'] = 'Digite um CPF válido'
        elif len(self.cpf) == 11:
            self.cpf = formata_documento(self.cpf, 'cpf')
            if not checar_validade(self.cpf):
                error_messages['cpf'] = 'Digite um CPF válido'
        else:
            error_messages['cpf'] = 'Digite um CPF válido'

        if error_messages:
            raise ValidationError(error_messages)

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
    cep = models.CharField(max_length=9, verbose_name='CEP')
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

    # Override clean function to validate CEP
    def clean(self):
        error_messages = {}
        if len(self.cep) == 9:
            if not checar_cep(self.cep):
                error_messages['cep'] = 'Digite um CEP válido'
        elif len(self.cep) == 8:
            self.cep = formata_cep(self.cep)
            if not checar_cep(self.cep):
                error_messages['cep'] = 'Digite um CEP válido'
        else:
            error_messages['cep'] = 'Digite um CEP válido'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta():
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
