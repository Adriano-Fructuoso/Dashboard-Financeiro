-- =====================================================
-- LIMPEZA E OTIMIZAÇÃO COMPLETA DO BANCO DE DADOS
-- DASHBOARD FINANCEIRO - MÚLTIPLOS USUÁRIOS
-- =====================================================

-- =====================================================
-- 1. LIMPEZA COMPLETA - REMOVER TODOS OS DADOS
-- =====================================================

-- Desabilitar triggers temporariamente
DROP TRIGGER IF EXISTS trigger_calcular_campos_tempo ON transacoes;

-- Limpar todas as tabelas
TRUNCATE TABLE transacoes CASCADE;
TRUNCATE TABLE usuarios CASCADE;

-- Resetar sequências
ALTER SEQUENCE usuarios_id_seq RESTART WITH 1;
ALTER SEQUENCE transacoes_id_seq RESTART WITH 1;

-- =====================================================
-- 2. RECRIAR ESTRUTURA OTIMIZADA
-- =====================================================

-- Remover tabelas antigas (se existirem)
DROP TABLE IF EXISTS lancamentos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS transacoes CASCADE;

-- Remover views antigas
DROP VIEW IF EXISTS resumo_mensal CASCADE;
DROP VIEW IF EXISTS categorias_populares CASCADE;

-- Remover funções antigas
DROP FUNCTION IF EXISTS calcular_campos_tempo() CASCADE;

-- =====================================================
-- 3. TABELA DE USUÁRIOS (OTIMIZADA)
-- =====================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE, -- Campo opcional para futuro
    ativo BOOLEAN DEFAULT TRUE, -- Para desativar usuários
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. TABELA DE TRANSAÇÕES (OTIMIZADA)
-- =====================================================
CREATE TABLE transacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data DATE NOT NULL,
    descricao VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Receita', 'Despesa')),
    valor DECIMAL(10,2) NOT NULL CHECK (valor > 0),
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes >= 1 AND mes <= 12),
    mes_ano VARCHAR(7) NOT NULL, -- formato: '2025-06'
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 5. ÍNDICES OTIMIZADOS PARA PERFORMANCE
-- =====================================================

-- Índices principais
CREATE INDEX idx_transacoes_usuario_id ON transacoes(usuario_id);
CREATE INDEX idx_transacoes_data ON transacoes(data);
CREATE INDEX idx_transacoes_tipo ON transacoes(tipo);
CREATE INDEX idx_transacoes_categoria ON transacoes(categoria);
CREATE INDEX idx_transacoes_ano ON transacoes(ano);
CREATE INDEX idx_transacoes_mes ON transacoes(mes);
CREATE INDEX idx_transacoes_mes_ano ON transacoes(mes_ano);

-- Índices compostos para consultas frequentes
CREATE INDEX idx_transacoes_usuario_data ON transacoes(usuario_id, data DESC);
CREATE INDEX idx_transacoes_usuario_tipo ON transacoes(usuario_id, tipo);
CREATE INDEX idx_transacoes_usuario_categoria ON transacoes(usuario_id, categoria);
CREATE INDEX idx_transacoes_usuario_mes_ano ON transacoes(usuario_id, mes_ano DESC);

-- Índices para usuários
CREATE INDEX idx_usuarios_nome ON usuarios(nome);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);

-- =====================================================
-- 6. FUNÇÕES E TRIGGERS OTIMIZADOS
-- =====================================================

-- Função para calcular campos de tempo automaticamente
CREATE OR REPLACE FUNCTION calcular_campos_tempo()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ano := EXTRACT(YEAR FROM NEW.data);
    NEW.mes := EXTRACT(MONTH FROM NEW.data);
    NEW.mes_ano := TO_CHAR(NEW.data, 'YYYY-MM');
    NEW.data_atualizacao := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular campos automaticamente
CREATE TRIGGER trigger_calcular_campos_tempo
    BEFORE INSERT OR UPDATE ON transacoes
    FOR EACH ROW
    EXECUTE FUNCTION calcular_campos_tempo();

-- Função para atualizar data_atualizacao em usuários
CREATE OR REPLACE FUNCTION atualizar_data_usuario()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para usuários
CREATE TRIGGER trigger_atualizar_usuario
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_data_usuario();

-- =====================================================
-- 7. VIEWS OTIMIZADAS PARA ANÁLISES
-- =====================================================

-- View para resumo mensal por usuário
CREATE OR REPLACE VIEW resumo_mensal AS
SELECT 
    t.usuario_id,
    u.nome as nome_usuario,
    t.ano,
    t.mes,
    t.mes_ano,
    SUM(CASE WHEN t.tipo = 'Receita' THEN t.valor ELSE 0 END) as total_receitas,
    SUM(CASE WHEN t.tipo = 'Despesa' THEN t.valor ELSE 0 END) as total_despesas,
    SUM(CASE WHEN t.tipo = 'Receita' THEN t.valor ELSE -t.valor END) as saldo,
    COUNT(*) as total_transacoes,
    COUNT(CASE WHEN t.tipo = 'Receita' THEN 1 END) as qtd_receitas,
    COUNT(CASE WHEN t.tipo = 'Despesa' THEN 1 END) as qtd_despesas
FROM transacoes t
JOIN usuarios u ON t.usuario_id = u.id
WHERE u.ativo = TRUE
GROUP BY t.usuario_id, u.nome, t.ano, t.mes, t.mes_ano
ORDER BY t.usuario_id, t.ano DESC, t.mes DESC;

-- View para categorias mais usadas por usuário
CREATE OR REPLACE VIEW categorias_populares AS
SELECT 
    t.usuario_id,
    u.nome as nome_usuario,
    t.categoria,
    t.tipo,
    COUNT(*) as quantidade,
    SUM(t.valor) as valor_total,
    AVG(t.valor) as valor_medio
FROM transacoes t
JOIN usuarios u ON t.usuario_id = u.id
WHERE u.ativo = TRUE
GROUP BY t.usuario_id, u.nome, t.categoria, t.tipo
ORDER BY t.usuario_id, quantidade DESC;

-- View para resumo geral por usuário
CREATE OR REPLACE VIEW resumo_geral_usuarios AS
SELECT 
    u.id,
    u.nome,
    u.email,
    u.ativo,
    u.data_criacao,
    COUNT(t.id) as total_transacoes,
    SUM(CASE WHEN t.tipo = 'Receita' THEN t.valor ELSE 0 END) as total_receitas,
    SUM(CASE WHEN t.tipo = 'Despesa' THEN t.valor ELSE 0 END) as total_despesas,
    SUM(CASE WHEN t.tipo = 'Receita' THEN t.valor ELSE -t.valor END) as saldo_geral,
    MAX(t.data) as ultima_transacao,
    MIN(t.data) as primeira_transacao
FROM usuarios u
LEFT JOIN transacoes t ON u.id = t.usuario_id
GROUP BY u.id, u.nome, u.email, u.ativo, u.data_criacao
ORDER BY u.nome;

-- =====================================================
-- 8. FUNÇÕES ÚTEIS PARA CONSULTAS
-- =====================================================

-- Função para obter saldo atual de um usuário
CREATE OR REPLACE FUNCTION obter_saldo_usuario(p_usuario_id INTEGER)
RETURNS DECIMAL AS $$
DECLARE
    saldo DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END), 0)
    INTO saldo
    FROM transacoes
    WHERE usuario_id = p_usuario_id;
    
    RETURN saldo;
END;
$$ LANGUAGE plpgsql;

-- Função para obter estatísticas de um usuário
CREATE OR REPLACE FUNCTION estatisticas_usuario(p_usuario_id INTEGER)
RETURNS TABLE(
    total_transacoes BIGINT,
    total_receitas DECIMAL,
    total_despesas DECIMAL,
    saldo DECIMAL,
    media_receitas DECIMAL,
    media_despesas DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT,
        COALESCE(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END), 0),
        COALESCE(AVG(CASE WHEN tipo = 'Receita' THEN valor END), 0),
        COALESCE(AVG(CASE WHEN tipo = 'Despesa' THEN valor END), 0)
    FROM transacoes
    WHERE usuario_id = p_usuario_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 9. CONSTRAINTS E VALIDAÇÕES ADICIONAIS
-- =====================================================

-- Constraint para garantir que usuário existe
ALTER TABLE transacoes 
ADD CONSTRAINT fk_transacoes_usuario 
FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE;

-- Constraint para valores positivos
ALTER TABLE transacoes 
ADD CONSTRAINT check_valor_positivo 
CHECK (valor > 0);

-- Constraint para datas válidas
ALTER TABLE transacoes 
ADD CONSTRAINT check_data_valida 
CHECK (data >= '2020-01-01' AND data <= '2030-12-31');

-- =====================================================
-- 10. COMENTÁRIOS E DOCUMENTAÇÃO
-- =====================================================

COMMENT ON TABLE usuarios IS 'Tabela de usuários do sistema financeiro';
COMMENT ON TABLE transacoes IS 'Tabela principal de transações financeiras';
COMMENT ON VIEW resumo_mensal IS 'Resumo mensal de transações por usuário';
COMMENT ON VIEW categorias_populares IS 'Categorias mais utilizadas por usuário';
COMMENT ON VIEW resumo_geral_usuarios IS 'Resumo geral de todos os usuários';

COMMENT ON COLUMN usuarios.nome IS 'Nome único do usuário';
COMMENT ON COLUMN usuarios.email IS 'Email opcional do usuário';
COMMENT ON COLUMN usuarios.ativo IS 'Status ativo/inativo do usuário';
COMMENT ON COLUMN transacoes.usuario_id IS 'ID do usuário proprietário da transação';
COMMENT ON COLUMN transacoes.valor IS 'Valor da transação (sempre positivo)';
COMMENT ON COLUMN transacoes.ano IS 'Ano calculado automaticamente da data';
COMMENT ON COLUMN transacoes.mes IS 'Mês calculado automaticamente da data';
COMMENT ON COLUMN transacoes.mes_ano IS 'Mês-Ano no formato YYYY-MM';

-- =====================================================
-- 11. VERIFICAÇÃO FINAL
-- =====================================================

-- Verificar se tudo foi criado corretamente
SELECT 
    'Estrutura do banco otimizada com sucesso!' as status,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public') as total_tabelas,
    (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public') as total_views,
    (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public') as total_funcoes;

-- Mostrar estrutura criada
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_type, table_name; 