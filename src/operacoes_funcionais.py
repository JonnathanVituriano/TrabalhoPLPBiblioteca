from functools import reduce

def filtrar_livros_por_categoria(livros, categoria):
    return tuple(filter(lambda livro: livro.categoria == categoria, livros))

def calcular_multa(dias_atraso, valor_diaria=2.0):
    if dias_atraso <= 0:
        return 0.0
    return float(dias_atraso * valor_diaria)

def filtrar_emprestimos_atrasados(emprestimos, data_referencia):
    return tuple(filter(lambda emp: emp.esta_atrasado(data_referencia), emprestimos))

def gerar_relatorio_multas(emprestimos, data_referencia, valor_diaria=2.0):
    atrasados = filtrar_emprestimos_atrasados(emprestimos, data_referencia)
    itens = tuple(map(
        lambda emp: {
            "identificador_emprestimo": emp.identificador,
            "titulo_livro": emp.livro.titulo,
            "nome_usuario": emp.usuario.nome,
            "dias_atraso": emp.dias_de_atraso(data_referencia),
            "valor_multa": calcular_multa(emp.dias_de_atraso(data_referencia), valor_diaria)
        },
        atrasados
    ))
    total_multas = reduce(lambda acumulador, item: acumulador + item["valor_multa"], itens, 0.0)
    return {
        "itens": itens,
        "total_multas": total_multas
    }

def contar_livros_por_categoria(livros):
    return reduce(
        lambda acumulador, livro: {
            **acumulador,
            livro.categoria: acumulador.get(livro.categoria, 0) + 1
        },
        livros,
        {}
    )

def contar_emprestimos_por_usuario(emprestimos):
    return reduce(
        lambda acumulador, emp: {
            **acumulador,
            emp.usuario.nome: acumulador.get(emp.usuario.nome, 0) + 1
        },
        emprestimos,
        {}
    )

def contar_emprestimos_ativos(emprestimos):
    return len(tuple(filter(lambda emp: emp.esta_ativo(), emprestimos)))

def contar_emprestimos_ativos_em_atraso(emprestimos, data_referencia):
    return len(tuple(filter(lambda emp: emp.esta_atrasado(data_referencia), emprestimos)))

def calcular_total_multas(emprestimos, data_referencia, valor_diaria=2.0):
    relatorio = gerar_relatorio_multas(emprestimos, data_referencia, valor_diaria)
    return relatorio["total_multas"]

def gerar_estatisticas_completas(livros, emprestimos, data_referencia, valor_diaria=2.0):
    return {
        "quantidade_livros_por_categoria": contar_livros_por_categoria(livros),
        "quantidade_emprestimos_por_usuario": contar_emprestimos_por_usuario(emprestimos),
        "quantidade_emprestimos_ativos": contar_emprestimos_ativos(emprestimos),
        "quantidade_emprestimos_ativos_em_atraso": contar_emprestimos_ativos_em_atraso(emprestimos, data_referencia),
        "valor_total_multas": calcular_total_multas(emprestimos, data_referencia, valor_diaria)
    }
