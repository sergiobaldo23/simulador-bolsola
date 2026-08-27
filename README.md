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

1. Clique em [`teste_estrategia.html`](teste_estrategia.html) aqui na lista de
   arquivos
2. No canto superior direito, clique no botão de **download** (seta para baixo)
3. Dê duplo clique no arquivo baixado

Não clique em **Raw** — esse botão mostra o código em vez de abrir a página.

Ele tem 606 KB e carrega tudo dentro de si: dados, motor de cálculo e fontes.
Não precisa baixar o resto do repositório, não precisa instalar nada, não
precisa nem de internet. Funciona em modo avião, num pendrive, em qualquer
máquina com navegador.

---

## 2. Simulador Ação vs. Renda Fixa — `index.html`

Compare, para qualquer ação da B3, quatro caminhos ao longo do tempo: reinvestir
os dividendos na própria ação (DRIP), reinvestir no CDI, ficar só com a
valorização da cotação, ou ter deixado tudo em renda fixa. Aceita carteira com
vários ativos.

### Como abrir

Este **não** funciona com duplo clique, e vale entender por quê antes de tentar:
ele lê as cotações de 382 arquivos da pasta `data/`, e todo navegador bloqueia
essa leitura quando a página é aberta direto do disco. A tela abre, mas fica
vazia. Não é defeito — é uma trava de segurança do navegador.

A solução é servir a pasta por um endereço local. Três passos:

**1. Baixe o repositório inteiro** (cerca de 35 MB)

No topo desta página, botão verde **Code** → **Download ZIP**. Descompacte em
qualquer lugar.

**2. Abra o terminal dentro da pasta descompactada**

- **Windows:** na barra de endereço do Explorador de Arquivos, escreva `cmd` e
  tecle Enter
- **macOS:** clique com o botão direito na pasta → Serviços → Novo Terminal

**3. Rode um destes comandos**

```bash
python -m http.server 8000
```

```bash
npx serve -l 8000
```

Depois abra <http://localhost:8000> no navegador. Para encerrar, feche o
terminal.

O primeiro comando precisa de **Python**, o segundo de **Node.js**. No macOS e
no Linux o Python normalmente já vem instalado; no Windows, costuma não vir —
nesse caso, instale de [python.org/downloads](https://www.python.org/downloads/)
marcando a opção **"Add Python to PATH"** durante a instalação.

> Se isso for barreira demais, use a página **Teste sua estratégia** acima: ela
> é um arquivo só e abre com duplo clique, sem instalar nada.

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
