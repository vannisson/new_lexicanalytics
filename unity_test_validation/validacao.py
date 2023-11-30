def valida_email(email, dominios_permitidos):
    if "@" and ".com" in email:
        _, dominio = email.split("@")
        return dominio in dominios_permitidos
    
    else:
        return False

def teste_valida_email():

    dominios_permitidos = ["@gmail.com", "@hotmail.com", "@outlook.com"]

    assert valida_email("usuario@gmail.com", dominios_permitidos) == True
    assert valida_email("usuario@hotmail.com", dominios_permitidos) == True
    # assert valida_email("email@dominio") == False
    # assert valida_email("emailsemarroba.com") == False

def valida_texto(texto, comprimento_minimo):
    return len(texto) >=comprimento_minimo

def teste_valida_texto():
    assert valida_texto("texto valido",1) == True 

def teste_valida_texto_vazio(): #somente por clareza e manutenção de código, mas essa função pode ser unificada com a funcao teste_valida_texto
    assert valida_texto("", 0) == False