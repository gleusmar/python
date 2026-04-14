# Como rodar o autenticador com GitHub Actions

## Passo 1: Fazer push do código para o GitHub

```bash
git init
git add .
git commit -m "Adiciona workflow do GitHub Actions"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

## Passo 2: Configurar Secrets no GitHub

Vá ao seu repositório no GitHub e configure as seguintes secrets:

1. Acesse: `Settings` → `Secrets and variables` → `Actions`
2. Clique em `New repository secret` e adicione:

### Secrets necessários:

- **USUARIO**: Seu usuário do sistema (ex: `04957832188`)
- **SENHA**: Sua senha do sistema
- **CREDENTIALS3_JSON**: Conteúdo do arquivo `credentials3.json` (service account do Google Sheets)

### Como adicionar o arquivo JSON como secret:

Para o `credentials3.json`:
```bash
cat credentials3.json
# Copie todo o conteúdo e cole no campo "Value" do secret
```

**Importante**: O `credentials3.json` é um arquivo de service account do Google Sheets que contém as credenciais para acessar sua planilha. Certifique-se de que este arquivo tem permissão para acessar a planilha especificada no `sheetsApi.py`.

## Passo 3: Executar o Workflow

### Execução manual:
1. Vá para a aba `Actions` no seu repositório
2. Selecione `Autenticador Guias`
3. Clique em `Run workflow`
4. Escolha a branch `main`
5. Clique em `Run workflow`

### Execução agendada:
O workflow está configurado para rodar automaticamente de segunda a sexta às 8h (horário UTC). 
Para alterar o horário, edite o arquivo `.github/workflows/autenticador.yml` e modifique a linha:
```yaml
- cron: '0 8 * * 1-5'
```

Formato cron: `minuto hora dia mês dia_da_semana`
- Exemplo para rodar às 9h (UTC): `0 9 * * 1-5`
- Exemplo para rodar às 12h (UTC): `0 12 * * 1-5`

## Passo 4: Monitorar a execução

1. Vá para a aba `Actions`
2. Clique na execução mais recente
3. Você pode ver os logs em tempo real
4. O workflow tem timeout de 6 horas (limite máximo do GitHub Actions)

## Limitações

- **Tempo máximo**: 6 horas por execução (plano gratuito)
- **Armazenamento**: Os arquivos locais não persistem entre execuções
- **Custo**: Gratuito para repositórios públicos, 2000 minutos/mês para privados

## Testar localmente antes

Para testar localmente com as mesmas variáveis de ambiente:

```bash
export USUARIO="seu_usuario"
export SENHA="sua_senha"
python test.py
```

## Troubleshooting

### Erro: Chrome não encontrado
O workflow instala automaticamente o Chrome e ChromeDriver no Ubuntu.

### Erro: Credenciais inválidas
Verifique se o secret `CREDENTIALS3_JSON` foi configurado corretamente e se o conteúdo do arquivo foi copiado integralmente. Certifique-se também de que o service account tem permissão para acessar a planilha do Google Sheets.

### Timeout
Se o script demorar mais de 6 horas, considere:
- Processar menos guias por execução
- Usar um servidor dedicado (VPS) em vez do GitHub Actions
