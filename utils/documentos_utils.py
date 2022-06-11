import re
import numpy as np
import random


def validar_mascara(documento):
    if re.match("([0-9]{3}).([0-9]{3}).([0-9]{3})-([0-9]{2})", documento):
        return 'cpf'
    elif re.match("([0-9]{2}).([0-9]{3}).([0-9]{3})/([0-9]{4})-([0-9]{2})", documento):
        return 'cnpj'
    else:
        return None


def remover_caracteres(documento):
    return re.sub(r'[^0-9]', '', documento)


def gerar_coeficiente(tipo):
    if len(tipo) == 9:  # Fase 1 cpf
        coef = np.arange(10, 1, -1)
        return coef
    elif len(tipo) == 12:  # Fase 1 cnpj
        coef1 = np.arange(5, 1, -1)
        coef2 = np.arange(9, 1, -1)
        coef = np.concatenate([coef1, coef2])
        return coef
    elif len(tipo) == 10:  # Fase 2 cpf
        coef = np.arange(11, 1, -1)
        return coef
    elif len(tipo) == 13:  # Fase 2 cnpj
        coef1 = np.arange(6, 1, -1)
        coef2 = np.arange(9, 1, -1)
        coef = np.concatenate([coef1, coef2])
        return coef
    else:
        return None


def calcular_digitos(documento, validar=True, tipo=None):
    if validar == True:
        tipo_doc = validar_mascara(documento)
        documento = remover_caracteres(documento)
    else:
        tipo_doc = tipo

    if not tipo_doc:
        raise ValueError()
    else:
        original_array = np.array(list(map(int, documento)))
        documento_array = np.array(list(map(int, documento[0:-2])))
        # Gerando e adicionando primeiro digito
        coeficiente = gerar_coeficiente(documento_array)
        documento_sum_dig1 = np.sum(documento_array * coeficiente)
        dig1 = 11 - (documento_sum_dig1 % 11)
        if dig1 <= 9:
            documento_array = np.append(documento_array, dig1)
        else:
            documento_array = np.append(documento_array, 0)

        # Gerando e adicionando segundo digito
        coeficiente2 = gerar_coeficiente(documento_array)
        documento_sum_dig2 = np.sum(documento_array * coeficiente2)
        dig2 = 11 - (documento_sum_dig2 % 11)
        if dig2 <= 9:
            documento_array = np.append(documento_array, dig2)
        else:
            documento_array = np.append(documento_array, 0)

        resultado = (list(original_array), list(documento_array))

        # Retorna uma tupla com os valores (documento_informado, documento_calculado)
        return resultado


def checar_validade(documento):
    tipo_doc = validar_mascara(documento)
    if not tipo_doc:
        raise ValueError()
    else:
        informado, calculado = calcular_digitos(documento)
        if informado == calculado:
            return True
        else:
            return False


def formata_documento(documento, tipo):
    if tipo == 'cpf':
        formatado = f'{documento[0:3]}.{documento[3:6]}.{documento[6:9]}-{documento[9:11]}'
        return formatado
    if tipo == 'cnpj':
        formatado = f'{documento[0:2]}.{documento[2:5]}.{documento[5:8]}/{documento[8:12]}-{documento[12:15]}'
        return formatado
    else:
        return None

def gerar_documento(tipo):
    if tipo == 'cpf':
        documento=[]
        for x in range(0,11):
            documento.append(random.randint(0,9))
        documento = calcular_digitos(documento, validar=False, tipo='cpf')
        documento = ''.join(str(x) for x in documento[1])
        return documento
    elif tipo == 'cnpj':
        documento=[]
        for x in range(0,14):
            documento.append(random.randint(0,9))
        documento = calcular_digitos(documento, validar=False, tipo='cnpj')
        documento = ''.join(str(x) for x in documento[1])
        return documento
    else:
        return None

def formata_cep(cep):
    formatado = f'{cep[0:6]}-{6:8}'
    return formatado

def checar_cep(cep):
    if re.search(r'^[^0-9]', self.cep) or len(self.cep) < 8:
        return False
    return True
