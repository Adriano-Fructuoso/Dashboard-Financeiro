-- ========================================
-- CONFIGURAÇÃO DO BANCO DE DADOS SUPABASE
-- ========================================
-- Execute estes comandos no SQL Editor do Supabase

-- 1. Criar tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Criar tabela de lançamentos financeiros
CREATE TABLE lancamentos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    data DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Receita', 'Despesa')),
    valor DECIMAL(10,2) NOT NULL CHECK (valor >= 0),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Criar índices para melhor performance
CREATE INDEX idx_lancamentos_usuario_id ON lancamentos(usuario_id);
CREATE INDEX idx_lancamentos_data ON lancamentos(data);
CREATE INDEX idx_lancamentos_tipo ON lancamentos(tipo);
CREATE INDEX idx_lancamentos_categoria ON lancamentos(categoria);

-- 4. Criar função para atualizar data_atualizacao automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 5. Criar triggers para atualizar data_atualizacao
CREATE TRIGGER update_usuarios_updated_at 
    BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lancamentos_updated_at 
    BEFORE UPDATE ON lancamentos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 6. Configurar Row Level Security (RLS) para segurança
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE lancamentos ENABLE ROW LEVEL SECURITY;

-- 7. Criar políticas de segurança para usuários
CREATE POLICY "Usuários podem ver apenas seus próprios dados" ON usuarios
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Usuários podem inserir seus próprios dados" ON usuarios
    FOR INSERT WITH CHECK (auth.uid()::text = id::text);

CREATE POLICY "Usuários podem atualizar seus próprios dados" ON usuarios
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 8. Criar políticas de segurança para lançamentos
CREATE POLICY "Usuários podem ver apenas seus próprios lançamentos" ON lancamentos
    FOR SELECT USING (
        usuario_id IN (
            SELECT id FROM usuarios WHERE id = usuario_id
        )
    );

CREATE POLICY "Usuários podem inserir seus próprios lançamentos" ON lancamentos
    FOR INSERT WITH CHECK (
        usuario_id IN (
            SELECT id FROM usuarios WHERE id = usuario_id
        )
    );

CREATE POLICY "Usuários podem atualizar seus próprios lançamentos" ON lancamentos
    FOR UPDATE USING (
        usuario_id IN (
            SELECT id FROM usuarios WHERE id = usuario_id
        )
    );

CREATE POLICY "Usuários podem deletar seus próprios lançamentos" ON lancamentos
    FOR DELETE USING (
        usuario_id IN (
            SELECT id FROM usuarios WHERE id = usuario_id
        )
    );

-- 9. Inserir usuário padrão (opcional)
-- INSERT INTO usuarios (nome, senha_hash) VALUES ('Adriano', '142536');

-- ========================================
-- COMANDOS PARA VERIFICAR A CONFIGURAÇÃO
-- ========================================

-- Verificar se as tabelas foram criadas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name IN ('usuarios', 'lancamentos');

-- Verificar se os índices foram criados
SELECT indexname, tablename FROM pg_indexes 
WHERE tablename IN ('usuarios', 'lancamentos');

-- Verificar se as políticas RLS foram criadas
SELECT schemaname, tablename, policyname FROM pg_policies 
WHERE tablename IN ('usuarios', 'lancamentos'); 