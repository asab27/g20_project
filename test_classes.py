# -*- coding: utf-8 -*-

from classes.agent import Agent
#from classes.solution import Solution
#from classes.ticket import Ticket
#from classes.ticket_assignment import TicketAssignment
import datetime

test_class = Agent
ob = '101;João Pereira;TI;joao@empresa.com'
db = 'data/tech_support.db'
test_class.read(db)

#test_class = Solution
#ob = '500;1;Reinício do router;2025-01-12'
#db = 'data/tech_support.db'
#test_class.read(db)

#test_class = Ticket
#ob = '1;Internet lenta;2025-01-10;Open'
#db = 'data/tech_support.db'
#test_class.read(db)

#test_class = TicketAssignment
#ob = '1;101;2025-01-10;45'
#db = 'data/tech_support.db'
#test_class.read(db)

op = ''
while op != 'q':
    print("\nEscolhe uma opção:")
    print("l - listar todos")
    print("b - início | n - seguinte | p - anterior | e - fim")
    print("i - inserir | m - modificar | r - remover")
    print("s - ordenar por atributo | f - procurar por atributo")
    print("q - sair")
    
    p = test_class.current()
    print(f"\nRegisto atual: {p}")
    op = input('> ').lower()

    if op == 'b':
        test_class.first()
    elif op == 'n':
        test_class.nextrec()
    elif op == 'p':
        test_class.previous()
    elif op == 'e':
        test_class.last()
    elif op == 'i':
        p1 = None
        if len(test_class.lst) == 0:
            p = eval(f'test_class.from_string("{ob}")')
            p1 = p
        str_list = list(p.__dict__.keys())
        attrib = str_list[0]
        atype = type(getattr(p, attrib))
        print('Deixa em branco para auto-incremento:')
        id = input(f'{attrib} = ')
        id = int(id) if id else 0
        strarg = f'test_class({id}'
        for i in range(1, len(str_list)):
            att = str_list[i]
            atype = type(getattr(p, att))
            if atype == datetime.date or atype == str:
                value = input(f'{att} = ')
                strarg += f',"{value}"'
            else:
                value = atype(input(f'{att} = '))
                strarg += f',{value}'
        strarg += ')'
        if p1:
            test_class.remove(getattr(p, str_list[0]))
        pobj = eval(strarg)
        code = getattr(pobj, str_list[0])
        test_class.insert(code)
    elif op == 'm':
        str_list = list(p.__dict__.keys())
        attrib = str_list[0]
        id = input(f'Registo {attrib} = ')
        if id:
            id = int(id)
            obj = test_class.current(id)
            print('Deixa em branco para manter valor atual:')
            for att in str_list[1:]:
                value = input(f'{att} = ')
                if value:
                    atype = type(getattr(obj, att))
                    if atype == datetime.date:
                        setattr(obj, att, datetime.date.fromisoformat(value))
                    else:
                        setattr(obj, att, atype(value))
            test_class.update(id)
    elif op == 'r':
        str_list = list(p.__dict__.keys())
        attrib = str_list[0]
        atype = type(getattr(p, attrib))
        cod = atype(input(f'{attrib} = '))
        if cod in test_class.lst:
            print(test_class.obj[cod])
            if input('Confirmar remoção (s/n)? ').lower() == 's':
                test_class.remove(cod)
    elif op == 'l':
        for code in test_class.lst:
            print(test_class.obj[code])
    elif op == 's':
        attrib = input('Ordenar por: ')
        if attrib in list(p.__dict__.keys()):
            reverse = input('Ordem inversa (s/n)? ').lower() == 's'
            codep = getattr(p, test_class.att[0])
            test_class.sort(attrib, reverse)
            for code in test_class.lst:
                print(test_class.obj[code])
            test_class.current(codep)
    elif op == 'f':
        attrib = input('Procurar por atributo: ')
        if attrib in list(p.__dict__.keys()):
            atype = type(getattr(p, attrib))
            value = atype(input('Valor a procurar: '))
            fobjs = test_class.find(value, attrib)
            if fobjs:
                test_class.current(getattr(fobjs[0], test_class.att[0]))
                for obj in fobjs:
                    print(obj)
