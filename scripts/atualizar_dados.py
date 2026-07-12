# -*- coding: utf-8 -*-
"""
Atualiza incrementalmente os arquivos data/{TICKER}.json com as cotacoes e
dividendos mais recentes do Yahoo Finance. Roda de forma independente do
projeto BolsaQuant_v3 (nao depende do banco SQLite local) — pensado para
rodar dentro do GitHub Actions, mas funciona local tambem.

Para cada ticker listado em data/_tickers.json:
  1. Le o JSON existente e descobre a ultima data ja salva.
  2. Busca no Yahoo Finance somente os dias NOVOS (a partir do dia seguinte).
  3. Acrescenta as novas datas/precos/dividendos ao arquivo, sem reescrever
     o historico antigo.

Uso:
    python scripts/atualizar_dados.py            # atualiza todos os tickers
    python scripts/atualizar_dados.py PETR4 VALE3  # so os tickers indicados
"""
import json
import os
import sys
import time

import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def carregar_ticker(caminho):
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)


def salvar_ticker(caminho, payload):
    s = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(s)


def atualizar_um(ticker):
    """Retorna (ticker, linhas_novas, erro_ou_None)."""
    caminho = os.path.join(DATA_DIR, ticker + '.json')
    if not os.path.exists(caminho):
        return ticker, 0, 'arquivo nao existe (ativo novo precisa de extracao completa)'

    payload = carregar_ticker(caminho)
    datas_existentes = payload['d']
    ultima_data = datas_existentes[-1] if datas_existentes else '2010-01-01'

    # Busca a partir do dia seguinte a ultima data salva
    import datetime
    dt_ini = datetime.date.fromisoformat(ultima_data) + datetime.timedelta(days=1)
    dt_hoje = datetime.date.today()
    if dt_ini > dt_hoje:
        return ticker, 0, None  # ja esta em dia

    try:
        hist = yf.Ticker(ticker + '.SA').history(
            start=dt_ini.isoformat(), auto_adjust=False, actions=True)
    except Exception as e:
        return ticker, 0, f'erro yfinance: {e}'

    if hist.empty:
        return ticker, 0, None  # sem pregoes novos (feriado/fim de semana/nao listado ainda)

    hist = hist.reset_index()
    if str(hist['Date'].dtype).startswith('datetime64[ns,'):
        hist['Date'] = hist['Date'].dt.tz_localize(None)
    hist['DateStr'] = hist['Date'].dt.strftime('%Y-%m-%d')

    # So aceita linhas estritamente APOS a ultima data ja salva (evita duplicar
    # caso o Yahoo devolva o proprio dia de "ultima_data" de novo)
    hist = hist[hist['DateStr'] > ultima_data]
    if hist.empty:
        return ticker, 0, None

    # Acesso por nome de coluna explicito (NAO por posicao/itertuples) — evita
    # o bug de indices trocados se a ordem das colunas do yfinance mudar.
    idx_base = len(datas_existentes)
    novos_div = {}
    datas_novas = hist['DateStr'].tolist()
    close_adj = hist['Adj Close'].tolist()
    close_raw = hist['Close'].tolist()
    divs = hist['Dividends'].tolist()
    for i in range(len(hist)):
        payload['d'].append(datas_novas[i])
        payload['c'].append(round(float(close_adj[i]), 4))
        payload['r'].append(round(float(close_raw[i]), 4))
        if divs[i] and divs[i] > 0:
            novos_div[str(idx_base + i)] = round(float(divs[i]), 6)

    payload['div'].update(novos_div)
    salvar_ticker(caminho, payload)
    return ticker, len(hist), None


def main():
    alvo = sys.argv[1:]
    if alvo:
        tickers = [t.upper().replace('.SA', '') for t in alvo]
    else:
        with open(os.path.join(DATA_DIR, '_tickers.json'), encoding='utf-8') as f:
            tickers = json.load(f)

    print(f"[*] Atualizando {len(tickers)} tickers...")
    total_novas = 0
    erros = []
    atualizados = []

    for i, tk in enumerate(tickers):
        tk_res, n, err = atualizar_um(tk)
        if err:
            erros.append((tk_res, err))
        elif n > 0:
            atualizados.append((tk_res, n))
            total_novas += n
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{len(tickers)} processados...")
        time.sleep(0.05)  # gentileza com a API do Yahoo

    print(f"\n[OK] {len(atualizados)} tickers com dados novos ({total_novas} linhas no total)")
    if erros:
        print(f"[AVISO] {len(erros)} tickers com erro:")
        for tk, e in erros[:20]:
            print(f"    {tk}: {e}")

    # Sinaliza pro workflow se houve mudanca real (usado p/ decidir se commita)
    with open('_atualizacao_resultado.txt', 'w') as f:
        f.write(f"{len(atualizados)} tickers atualizados, {total_novas} linhas novas, {len(erros)} erros\n")


if __name__ == '__main__':
    main()
