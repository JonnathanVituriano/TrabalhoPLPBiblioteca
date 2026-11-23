from functools import reduce
from src.operacoes_funcionais import calcular_multa

def calcular_total_multas_imperativo(emprestimos, data_referencia, valor_diaria=2.0):
    total = 0.0
    for emp in emprestimos:
        if emp.esta_atrasado(data_referencia):
            dias = emp.dias_de_atraso(data_referencia)
            total += dias * valor_diaria
    return total

def calcular_total_multas_funcional(emprestimos, data_referencia, valor_diaria=2.0):
    atrasados = filter(lambda emp: emp.esta_atrasado(data_referencia), emprestimos)
    multas = map(lambda emp: calcular_multa(emp.dias_de_atraso(data_referencia), valor_diaria), atrasados)
    return reduce(lambda acumulador, multa: acumulador + multa, multas, 0.0)
