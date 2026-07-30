from lista_contatos.interface import Interface
from lista_contatos.repositorio import RepositorioJson
from lista_contatos.agenda import Agenda

def main():
    repositorio = RepositorioJson()
    agenda = Agenda(repositorio)
    app = Interface(agenda)

    app.mainloop()
    

if __name__ == "__main__":
    main()