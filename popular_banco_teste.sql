-- ========================================
-- SCRIPT PARA POPULAR BANCO COM DADOS DE TESTE
-- ========================================
-- Execute este script no SQL Editor do Supabase

-- 1. Primeiro, vamos criar um usuário de teste
INSERT INTO usuarios (nome, senha_hash) 
VALUES ('maria_silva', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')
ON CONFLICT (nome) DO NOTHING;

-- 2. Obter o ID do usuário criado
DO $$
DECLARE
    usuario_id INTEGER;
BEGIN
    SELECT id INTO usuario_id FROM usuarios WHERE nome = 'maria_silva';
    
    -- 3. Inserir receitas realistas (últimos 6 meses)
    
    -- Salário mensal
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-05', 'Salário Janeiro', 'Salário', 'Receita', 4500.00),
    (usuario_id, '2025-02-05', 'Salário Fevereiro', 'Salário', 'Receita', 4500.00),
    (usuario_id, '2025-03-05', 'Salário Março', 'Salário', 'Receita', 4500.00),
    (usuario_id, '2025-04-05', 'Salário Abril', 'Salário', 'Receita', 4500.00),
    (usuario_id, '2025-05-05', 'Salário Maio', 'Salário', 'Receita', 4500.00),
    (usuario_id, '2025-06-05', 'Salário Junho', 'Salário', 'Receita', 4500.00);
    
    -- Freelance/Projetos extras
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-15', 'Projeto freelance site', 'Freelance', 'Receita', 800.00),
    (usuario_id, '2025-02-20', 'Consultoria marketing', 'Freelance', 'Receita', 600.00),
    (usuario_id, '2025-03-10', 'Design logo empresa', 'Freelance', 'Receita', 400.00),
    (usuario_id, '2025-04-25', 'Projeto app mobile', 'Freelance', 'Receita', 1200.00),
    (usuario_id, '2025-05-18', 'Revisão textos', 'Freelance', 'Receita', 300.00),
    (usuario_id, '2025-06-12', 'Consultoria SEO', 'Freelance', 'Receita', 500.00);
    
    -- Investimentos
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-10', 'Dividendos ações', 'Investimentos', 'Receita', 150.00),
    (usuario_id, '2025-02-10', 'Dividendos ações', 'Investimentos', 'Receita', 180.00),
    (usuario_id, '2025-03-10', 'Dividendos ações', 'Investimentos', 'Receita', 120.00),
    (usuario_id, '2025-04-10', 'Dividendos ações', 'Investimentos', 'Receita', 200.00),
    (usuario_id, '2025-05-10', 'Dividendos ações', 'Investimentos', 'Receita', 160.00),
    (usuario_id, '2025-06-10', 'Dividendos ações', 'Investimentos', 'Receita', 190.00);
    
    -- 4. Inserir despesas realistas
    
    -- Moradia
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-02-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-03-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-04-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-05-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-06-10', 'Aluguel', 'Moradia', 'Despesa', 1200.00),
    (usuario_id, '2025-01-15', 'Conta de luz', 'Moradia', 'Despesa', 180.00),
    (usuario_id, '2025-02-15', 'Conta de luz', 'Moradia', 'Despesa', 160.00),
    (usuario_id, '2025-03-15', 'Conta de luz', 'Moradia', 'Despesa', 140.00),
    (usuario_id, '2025-04-15', 'Conta de luz', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-05-15', 'Conta de luz', 'Moradia', 'Despesa', 100.00),
    (usuario_id, '2025-06-15', 'Conta de luz', 'Moradia', 'Despesa', 90.00),
    (usuario_id, '2025-01-20', 'Conta de água', 'Moradia', 'Despesa', 80.00),
    (usuario_id, '2025-02-20', 'Conta de água', 'Moradia', 'Despesa', 85.00),
    (usuario_id, '2025-03-20', 'Conta de água', 'Moradia', 'Despesa', 75.00),
    (usuario_id, '2025-04-20', 'Conta de água', 'Moradia', 'Despesa', 90.00),
    (usuario_id, '2025-05-20', 'Conta de água', 'Moradia', 'Despesa', 70.00),
    (usuario_id, '2025-06-20', 'Conta de água', 'Moradia', 'Despesa', 80.00),
    (usuario_id, '2025-01-25', 'Internet', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-02-25', 'Internet', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-03-25', 'Internet', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-04-25', 'Internet', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-05-25', 'Internet', 'Moradia', 'Despesa', 120.00),
    (usuario_id, '2025-06-25', 'Internet', 'Moradia', 'Despesa', 120.00);
    
    -- Alimentação
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-05', 'Supermercado', 'Alimentação', 'Despesa', 450.00),
    (usuario_id, '2025-01-15', 'Supermercado', 'Alimentação', 'Despesa', 380.00),
    (usuario_id, '2025-01-25', 'Supermercado', 'Alimentação', 'Despesa', 420.00),
    (usuario_id, '2025-02-05', 'Supermercado', 'Alimentação', 'Despesa', 400.00),
    (usuario_id, '2025-02-15', 'Supermercado', 'Alimentação', 'Despesa', 350.00),
    (usuario_id, '2025-02-25', 'Supermercado', 'Alimentação', 'Despesa', 430.00),
    (usuario_id, '2025-03-05', 'Supermercado', 'Alimentação', 'Despesa', 410.00),
    (usuario_id, '2025-03-15', 'Supermercado', 'Alimentação', 'Despesa', 390.00),
    (usuario_id, '2025-03-25', 'Supermercado', 'Alimentação', 'Despesa', 440.00),
    (usuario_id, '2025-04-05', 'Supermercado', 'Alimentação', 'Despesa', 420.00),
    (usuario_id, '2025-04-15', 'Supermercado', 'Alimentação', 'Despesa', 380.00),
    (usuario_id, '2025-04-25', 'Supermercado', 'Alimentação', 'Despesa', 450.00),
    (usuario_id, '2025-05-05', 'Supermercado', 'Alimentação', 'Despesa', 400.00),
    (usuario_id, '2025-05-15', 'Supermercado', 'Alimentação', 'Despesa', 370.00),
    (usuario_id, '2025-05-25', 'Supermercado', 'Alimentação', 'Despesa', 420.00),
    (usuario_id, '2025-06-05', 'Supermercado', 'Alimentação', 'Despesa', 430.00),
    (usuario_id, '2025-06-15', 'Supermercado', 'Alimentação', 'Despesa', 390.00),
    (usuario_id, '2025-06-25', 'Supermercado', 'Alimentação', 'Despesa', 410.00);
    
    -- Restaurantes
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-08', 'Restaurante com amigos', 'Alimentação', 'Despesa', 85.00),
    (usuario_id, '2025-01-18', 'Delivery pizza', 'Alimentação', 'Despesa', 45.00),
    (usuario_id, '2025-02-12', 'Café da manhã', 'Alimentação', 'Despesa', 25.00),
    (usuario_id, '2025-02-22', 'Almoço trabalho', 'Alimentação', 'Despesa', 35.00),
    (usuario_id, '2025-03-08', 'Jantar família', 'Alimentação', 'Despesa', 120.00),
    (usuario_id, '2025-03-18', 'Delivery sushi', 'Alimentação', 'Despesa', 65.00),
    (usuario_id, '2025-04-12', 'Café com cliente', 'Alimentação', 'Despesa', 30.00),
    (usuario_id, '2025-04-28', 'Almoço fim de semana', 'Alimentação', 'Despesa', 55.00),
    (usuario_id, '2025-05-10', 'Jantar aniversário', 'Alimentação', 'Despesa', 95.00),
    (usuario_id, '2025-05-20', 'Delivery hambúrguer', 'Alimentação', 'Despesa', 40.00),
    (usuario_id, '2025-06-08', 'Almoço com colegas', 'Alimentação', 'Despesa', 50.00),
    (usuario_id, '2025-06-18', 'Café tarde', 'Alimentação', 'Despesa', 20.00);
    
    -- Transporte
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-05', 'Combustível', 'Transporte', 'Despesa', 200.00),
    (usuario_id, '2025-01-20', 'Combustível', 'Transporte', 'Despesa', 180.00),
    (usuario_id, '2025-02-05', 'Combustível', 'Transporte', 'Despesa', 190.00),
    (usuario_id, '2025-02-20', 'Combustível', 'Transporte', 'Despesa', 170.00),
    (usuario_id, '2025-03-05', 'Combustível', 'Transporte', 'Despesa', 210.00),
    (usuario_id, '2025-03-20', 'Combustível', 'Transporte', 'Despesa', 185.00),
    (usuario_id, '2025-02-15', 'Uber para reunião', 'Transporte', 'Despesa', 35.00),
    (usuario_id, '2025-03-10', 'Uber para aeroporto', 'Transporte', 'Despesa', 45.00),
    (usuario_id, '2025-04-05', 'Uber para shopping', 'Transporte', 'Despesa', 25.00),
    (usuario_id, '2025-05-15', 'Uber para médico', 'Transporte', 'Despesa', 30.00),
    (usuario_id, '2025-06-10', 'Uber para festa', 'Transporte', 'Despesa', 40.00);
    
    -- Saúde
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-02-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-03-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-04-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-05-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-06-10', 'Plano de saúde', 'Saúde', 'Despesa', 350.00),
    (usuario_id, '2025-02-15', 'Consulta médica', 'Saúde', 'Despesa', 120.00),
    (usuario_id, '2025-03-25', 'Exame de sangue', 'Saúde', 'Despesa', 85.00),
    (usuario_id, '2025-04-18', 'Consulta dentista', 'Saúde', 'Despesa', 150.00),
    (usuario_id, '2025-05-22', 'Medicamentos', 'Saúde', 'Despesa', 65.00),
    (usuario_id, '2025-06-05', 'Consulta oftalmologista', 'Saúde', 'Despesa', 180.00);
    
    -- Lazer
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-12', 'Cinema', 'Lazer', 'Despesa', 35.00),
    (usuario_id, '2025-01-28', 'Show de música', 'Lazer', 'Despesa', 120.00),
    (usuario_id, '2025-02-14', 'Jantar romântico', 'Lazer', 'Despesa', 180.00),
    (usuario_id, '2025-03-01', 'Teatro', 'Lazer', 'Despesa', 80.00),
    (usuario_id, '2025-03-15', 'Passeio no parque', 'Lazer', 'Despesa', 25.00),
    (usuario_id, '2025-04-05', 'Museu', 'Lazer', 'Despesa', 20.00),
    (usuario_id, '2025-04-20', 'Bar com amigos', 'Lazer', 'Despesa', 75.00),
    (usuario_id, '2025-05-08', 'Academia mensal', 'Lazer', 'Despesa', 120.00),
    (usuario_id, '2025-05-25', 'Passeio de fim de semana', 'Lazer', 'Despesa', 200.00),
    (usuario_id, '2025-06-12', 'Jogos online', 'Lazer', 'Despesa', 50.00),
    (usuario_id, '2025-06-28', 'Festival gastronômico', 'Lazer', 'Despesa', 150.00);
    
    -- Educação
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-15', 'Curso online Excel', 'Educação', 'Despesa', 150.00),
    (usuario_id, '2025-02-20', 'Livro técnico', 'Educação', 'Despesa', 85.00),
    (usuario_id, '2025-03-10', 'Workshop marketing digital', 'Educação', 'Despesa', 200.00),
    (usuario_id, '2025-04-05', 'Assinatura revista técnica', 'Educação', 'Despesa', 45.00),
    (usuario_id, '2025-05-15', 'Curso de inglês', 'Educação', 'Despesa', 300.00),
    (usuario_id, '2025-06-20', 'Certificação profissional', 'Educação', 'Despesa', 450.00);
    
    -- Vestuário
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-20', 'Roupas trabalho', 'Vestuário', 'Despesa', 250.00),
    (usuario_id, '2025-02-10', 'Tênis esportivo', 'Vestuário', 'Despesa', 180.00),
    (usuario_id, '2025-03-25', 'Acessórios', 'Vestuário', 'Despesa', 120.00),
    (usuario_id, '2025-04-15', 'Roupas casuais', 'Vestuário', 'Despesa', 200.00),
    (usuario_id, '2025-05-30', 'Roupa para evento', 'Vestuário', 'Despesa', 350.00),
    (usuario_id, '2025-06-18', 'Roupas de inverno', 'Vestuário', 'Despesa', 280.00);
    
    -- Outros
    INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor) VALUES
    (usuario_id, '2025-01-30', 'Presente aniversário', 'Outros', 'Despesa', 80.00),
    (usuario_id, '2025-02-28', 'Doação caridade', 'Outros', 'Despesa', 100.00),
    (usuario_id, '2025-03-20', 'Seguro residencial', 'Outros', 'Despesa', 120.00),
    (usuario_id, '2025-04-30', 'Presente mãe', 'Outros', 'Despesa', 150.00),
    (usuario_id, '2025-05-25', 'Taxa bancária', 'Outros', 'Despesa', 25.00),
    (usuario_id, '2025-06-30', 'Manutenção computador', 'Outros', 'Despesa', 200.00);
    
    RAISE NOTICE 'Dados inseridos com sucesso para o usuário ID: %', usuario_id;
    
END $$;

-- 5. Verificar os dados inseridos
SELECT 
    'Resumo dos dados inseridos' as info,
    COUNT(*) as total_transacoes,
    COUNT(CASE WHEN tipo = 'Receita' THEN 1 END) as total_receitas,
    COUNT(CASE WHEN tipo = 'Despesa' THEN 1 END) as total_despesas,
    SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END) as valor_total_receitas,
    SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END) as valor_total_despesas,
    SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END) as saldo
FROM transacoes t
JOIN usuarios u ON t.usuario_id = u.id
WHERE u.nome = 'maria_silva';

-- 6. Verificar distribuição por categoria
SELECT 
    categoria,
    tipo,
    COUNT(*) as quantidade,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM transacoes t
JOIN usuarios u ON t.usuario_id = u.id
WHERE u.nome = 'maria_silva'
GROUP BY categoria, tipo
ORDER BY tipo, valor_total DESC;

-- 7. Verificar distribuição mensal
SELECT 
    TO_CHAR(data, 'YYYY-MM') as mes_ano,
    COUNT(*) as total_transacoes,
    SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END) as receitas,
    SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END) as despesas,
    SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END) as saldo
FROM transacoes t
JOIN usuarios u ON t.usuario_id = u.id
WHERE u.nome = 'maria_silva'
GROUP BY TO_CHAR(data, 'YYYY-MM')
ORDER BY mes_ano; 