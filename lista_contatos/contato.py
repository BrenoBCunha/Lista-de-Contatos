import re

class Contato:
    def __init__(self, id_contato:int, nome:str, telefone:str, email:str = "", endereco:str = ""):
        self.__id_contato = id_contato
        self.atualizar(nome, telefone, email, endereco)


    @property
    def id(self):
        return self.__id_contato

    @property
    def nome(self):
        return self.__nome

    @property
    def telefone(self):
        return self.__telefone

    @property
    def email(self):
        return self.__email

    @property
    def endereco(self):
        return self.__endereco
    

    def atualizar(self, nome:str, telefone:str, email:str = "", endereco:str = ""):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        nome = nome.strip()
        telefone = telefone.strip()

        telefone = self.normalizar_telefone(telefone)

        if not nome:
            raise ValueError("Nome deve conter ao menos um caracter")

        if not telefone or len(telefone) != 11:
            raise ValueError("Telefone inválido. Siga o formato: (DDD)90000-0000")

        if email and not re.match(padrao, email) and email != "Email não cadastrado.":
            raise ValueError("Email deve seguir o padrão: seuemail@dominio.com")


        self.__nome = nome
        self.__telefone = telefone

        if not email:
            self.__email = None
        else:
            self.__email = email.strip()

        if not endereco:
            self.__endereco = None
        else:
            self.__endereco = endereco.strip()

    def editar(self, nome:str=None, telefone:str=None, email:str=None, endereco:str=None):
        
        if nome is None:
            nome = self.nome
        else:
            nome = nome.strip()
        if telefone is None:
            telefone = self.telefone
        else:
            telefone = telefone.strip()
        if email is None:
            email = self.email
        else:
            email = email.strip()
        if endereco is None:
            endereco = self.endereco
        else:
            endereco = endereco.strip()

        self.atualizar(nome, telefone, email, endereco)


    def normalizar_telefone(self, telefone):
        return "".join([char for char in telefone if char.isdigit()])


    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco
        }

    @classmethod
    def de_dict(cls, dado:dict):
        return cls(dado["id"], dado["nome"], dado["telefone"], dado["email"], dado["endereco"])


