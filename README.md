# Simulador B3

Duas ferramentas de bolsa, cada uma uma página web só. Dados da B3 vindos do
Yahoo Finance, atualizados automaticamente todo dia.

---

## 1. Teste sua estratégia — `teste_estrategia.html`

Escolha por quais indicadores fundamentalistas as ações da B3 devem ser
ranqueadas e o peso de cada um, defina o tamanho da carteira, e veja o que essa
regra teria feito com R$ 100.000 entre maio de 2011 e maio de 2026 — **60
rebalanceamentos trimestrais, líquido de imposto de renda**.

- 9 indicadores para marcar e desmarcar (P/VP, EV/EBITDA, Dívida Líq./EBITDA,
  Eficiência, Earnings Yield, Margem Bruta, Qualidade do Lucro, ROA, Dividendos),
  com peso livre em cada um
- Tamanho da carteira de 1 a 100 ações
- Gráfico do capital contra Ibovespa e CDI
- **Ficha de auditoria de cada rebalanceamento:** o que comprou, o que vendeu,
  preços, quantidades, proventos e o imposto apurado no ciclo
- **Selos de honestidade:** quantos ciclos a estratégia realmente operou, a
  cobertura de dado usada para decidir, e o Deflated Sharpe Ratio descontado
  pelo número de combinações testadas — o antídoto contra achar padrão onde só
  há sorte

### Como abrir

**Baixe só este arquivo e dê duplo clique.** É isso.

Ele tem 606 KB e carrega tudo dentro de si — dados, motor de cálculo e fontes.
Não precisa baixar o resto do repositório, não precisa instalar nada, não
precisa de internet. Funciona em modo avião, num pendrive, em qualquer máquina
com navegador.

Para baixar: abra o arquivo aqui no GitHub, clique no botão de download
(a seta para baixo, no canto superior direito do visualizador). Não use o botão
"Raw" — ele mostra o código em vez da página.

---

## 2. Simulador Ação vs. Renda Fixa — `index.html`

Compare, para qualquer ação da B3, quatro caminhos ao longo do tempo: reinvestir
os dividendos na própria ação (DRIP), reinvestir no CDI, ficar só com a
valorização da cotação, ou ter deixado tudo em renda fixa. Aceita carteira com
vários ativos.

### Como abrir

Este **não** funciona com duplo clique. Ele lê as cotações de 382 arquivos na
pasta `data/`, e navegadores bloqueiam essa leitura quando a página é aberta
direto do disco (`file://`). Você precisa de um servidor local:

```bash
# baixe o repositório inteiro (34 MB), entre na pasta e rode:
python -m http.server 8000
```

Depois abra `http://localhost:8000` no navegador. Com Node no lugar do Python,
`npx serve` faz o mesmo.

---

## De onde vêm os dados

- **Cotações e proventos:** Yahoo Finance, via `yfinance`. Uma rotina automática
  (`.github/workflows/atualizar_dados.yml`) roda todo dia às 21h30 e atualiza a
  pasta `data/`.
- **Indicadores fundamentalistas:** balanços trimestrais e anuais entregues à
  CVM (ITR e DFP), processados pelo motor do BolsaQuant.

Preços ajustados por provento e por desdobramento. O universo inclui empresas
que foram deslistadas no período, para o resultado não ficar inflado por só
olhar quem sobreviveu.

## Aviso

Isto é uma ferramenta de estudo, não recomendação de investimento. Resultado
passado não promete nada sobre o futuro — e a página inteira foi desenhada
justamente para deixar visível o quanto um backtest bonito pode ser sorte.
