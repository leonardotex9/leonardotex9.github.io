import pandas as pd
import numpy as np
import datetime
import locale
import re
import gc
import os
import matplotlib.pyplot as plt

from grafico_gerente_mensal import gerar_imagem_glm
from random import randint

pd.set_option('display.max_columns', None)

## Prêmio Gerente Mensal

# Definição do locale para utilizar formatação com separador de milhar como '.'
locale.setlocale(locale.LC_ALL, 'Portuguese')

## VARs

# Dicionário de apoio para ajustar a data na mensagem
month_dict = {
    1: 'jan',
    2: 'fev',
    3: 'mar',
    4: 'abr',
    5: 'mai',
    6: 'jun',
    7: 'jul',
    8: 'ago',
    9: 'set',
    10: 'out',
    11: 'nov',
    12: 'dez'
}

DT_TODAY = datetime.datetime.today().replace(day = 13)
DT_TODAY_FILE = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%Y.%m.%d')
DT_DIA = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%d')
DT_MES = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%m')
DATE_FILE = DT_TODAY.strftime('%Y%m%d')
REF_DATE = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%d/') + month_dict[DT_TODAY.month]

# # DT_NPS = DT_TODAY - datetime.timedelta(days = (DT_TODAY.weekday() + 3))
# DT_NPS = '01/jan'
# DT_CART = '03/fev'

# REF_DATE_NPS = DT_NPS.strftime('%d/') + month_dict[DT_NPS.month]
# REF_DATE_NPS = DT_NPS

# Função para acertar o emoji pra cada indicador
def get_emoji(cump):
    if cump >= 1:
        return '✅'
    elif cump >= 0.9:
        return '⚠'
    else:
        return '❌'

# Função para acertar o emoji para o NPS
def get_emoji_nps(cump):
    if cump >= 1:
        return '✅'
    else:
        return '❌'

# Função para acertar o emoji para os indicadores de família de serviços
def get_emoji_fam(cump):
    if cump >= 1:
        return '✅'
    elif cump >= 0.7:
        return '⚠'
    else:
        return '❌'

def get_espelhamento(df_print,df_esp,perfil):
    if perfil == 'VC':
        df_esp = df_esp[~df_esp['vendedor_comum'].isnull()][['username','vendedor_comum']].rename(columns={'username':'nome_usuario','vendedor_comum':'username'})
    elif perfil == 'VL':
        df_esp = df_esp[~df_esp['vendedor_lider'].isnull()][['username','vendedor_lider']].rename(columns={'username':'nome_usuario','vendedor_lider':'username'})
    elif perfil == 'GL':
        df_esp = df_esp[~df_esp['gerente_loja'].isnull()][['username','gerente_loja']].rename(columns={'username':'nome_usuario','gerente_loja':'username'})
    else:
        raise LOGGER.error('Perfil selecionado não listado')

    df_esp['username'] = df_esp['username'].astype(int).astype(str)
    df_esp = df_esp.merge(df_print, on = 'username', how = 'left')
    df_esp = df_esp.drop(columns='username').rename(columns={'nome_usuario':'username'})
    df_print = df_print.append(df_esp)

    return df_print

# Template da primeira metade do extrato do VL (Prêmio Líder Categoria)
TEMPLATE = """
Oi {nome}! Olha como está o desempenho da loja (até {data}) e a PROJEÇÃO da sua premiação mensal:

💰PRÊMIO PROJETADO: R${prem_loja}
 {emoji_merc_loja} Merc: {cump_merc_loja:.0f}% ➡️ 💰R${prem_merc_loja}
 ({criterio_merc})
 {emoji_serv_loja} Serv*: {cump_serv_loja:.0f}% ➡️ 💰R${prem_serv_loja}
 {emoji_cdc_loja} CDC: {cump_cdc_loja:.0f}% ➡️ 💰R${prem_cdc_loja}
 {emoji_mov} Móveis: {cump_mov:.0f}% ➡️ 💰R${prem_mov}
 {emoji_port} Portáteis: {cump_port:.0f}% ➡️ 💰R${prem_port}
 {emoji_cart} Cartões: {cump_cart:.0f}% ➡️ 💰R${prem_cart}
 (em {data_cart})
 {emoji_nps} NPS: {cump_nps:.0f}% ➡️ 💰R${prem_nps}
 (em {data_nps})

*Olha como estão as Famílias de Serviços (pré-req 70%):
 {emoji_fam1} Família 1: {cump_fam1:.0f}%
 {emoji_fam2} Família 2: {cump_fam2:.0f}%
 {emoji_fam3} Família 3: {cump_fam3:.0f}%
 {emoji_fam4} Família 4: {cump_fam4:.0f}%
 {emoji_fam5} Família 5: {cump_fam5:.0f}%
"""

TEMPLATE_URL = "https://bk9jvk64kh.execute-api.us-east-1.amazonaws.com/dev/gerente/grafico_mensal?cd_fun={cd_fun}&cd_fil={cd_fil}&fil_porte={fil_porte}&fil_perfil={fil_perfil}&merc_real={merc_real}&merc_meta_tot={merc_meta_tot}&merc_meta_acu={merc_meta_acu}&serv_real={serv_real}&serv_meta_tot={serv_meta_tot}&serv_meta_acu={serv_meta_acu}&cdc_real={cdc_real}&cdc_meta_tot={cdc_meta_tot}&cdc_meta_acu={cdc_meta_acu}&moveis_real={moveis_real}&moveis_meta_tot={moveis_meta_tot}&moveis_meta_acu={moveis_meta_acu}&port_real={port_real}&port_meta_tot={port_meta_tot}&port_meta_acu={port_meta_acu}&cartao_real={cartao_real}&cartao_meta_tot={cartao_meta_tot}&cartao_meta_acu={cartao_meta_acu}&fam_serv={fam_serv}&nps_real={nps_real}&nps_meta_tot={nps_meta_tot}&dia={dia}&mes={mes}"

df = pd.DataFrame([1,3],[2,4])

# Função para ajustar a data
def fix_date(timestamp):
    return str(timestamp.day) + '/' + month_dict[timestamp.month]

rename_dict = {
     'Estabelecimento': 'CD_FIL',
#      'Regional': 'CD_REG',
#      'Diretoria': 'CD_DIR',
     '% Eficiência Serviços Valor': 'ICM_SERV',
     '% Participação CDC Valor': 'ICM_CDC',
     '% Família 1 (Garantia Eletro + Garantia Moveis)': 'ICM_FAM1',
     '% Família 2 (VPP + Prot Financeira + Tecnico + Saúde Premiada)': 'ICM_FAM2',
     '% Família 3  (Residencial + Multiassistência)': 'ICM_FAM3',
     '% Família 4 (Fique Seguro)': 'ICM_FAM4',
#      '% Família 5 (Planos)': 'ICM_FAM5',
     '% Planos': 'ICM_FAM5',
     'PORTE': 'PORTE',
     'TARGET MENSAL': 'TARGET',
     'TIPO PAINEL': 'TIPO_META',
     'ICM Mercantil Final': 'ICM_MERC',
#      'Faixa Mercantil': 'FAIXA_MERC',
     'Peso Mercantil': 'PESO_MERC',
     'Payout Mercantil': 'PAY_MERC',
     'Prêmio Mercantil': 'PREM_MERC',
#      'Pré Requisito Famílias': 'N_PRQ_FAM',
     'Cumpr. Pré Requisito': 'FLAG_PRQ_FAM',
     'ICM Serviços Final': 'ICM_SERV_OFC',
#      'Faixa Serviços': 'FAIXA_SERV',
     'Peso Serviços': 'PESO_SERV',
     'Payout Serviços': 'PAY_SERV',
     'Prêmio Serviços': 'PREM_SERV',
#      'Faixa CDC': 'FAIXA_CDC',
     'Peso CDC': 'PESO_CDC',
     'Payout CDC': 'PAY_CDC',
     'Prêmio CDC': 'PREM_CDC',
     'ICM Móveis': 'ICM_MOV',
#      'Faixa Móveis': 'FAIXA_MOV',
     'Peso Móveis': 'PESO_MOV',
     'Payout Móveis': 'PAY_MOV',
     'Prêmio Móveis': 'PREM_MOV',
     'ICM Portáteis': 'ICM_PORT',
#      'Faixa Portáteis': 'FAIXA_TEL',
     'Peso Portatéis': 'PESO_PORT',
     'Payout Portáteis': 'PAY_PORT',
     'Prêmio Portáteis': 'PREM_PORT',
     'ICM Cartões': 'ICM_CART',
#      'Faixa Cartões': 'FAIXA_CART',
     'Peso Cartões': 'PESO_CART',
     'Payout Cartões': 'PAY_CART',
     'Prêmio Cartões': 'PREM_CART',
     'ICM NPS': 'ICM_NPS',
     'Prêmio NPS': 'PREM_NPS',
     'Prêmio TOTAL': 'PREM_TOT',
    'Data Atualziação NPS': 'DT_NPS',
    'Data Atualziação Cartões': 'DT_CART',
    'Critério Venda': 'CRITERIO_MERC',

    'Meta Venda Mercantil Total': 'MERC_META_TOT',
    'Meta Venda Mercantil': 'MERC_META_ACU',
    'Realizado Venda Mercantil': 'MERC_REAL',
    'Meta mercantil Total                       (Sem retira rápido)':'MERC_META_TOT_S_RET',
    'Meta Móveis        (Sem retira rápido)': 'MOVEIS_META_ACU_S_RET',
    'Meta Eletro           (Sem retira rápido)': 'PORT_META_ACU_S_RET',
    'Venda Móveis         ( Sem retira rápido )': 'MOVEIS_REAL_S_RET',
    'Venda Eletro           ( Sem retira rápido )': 'PORT_REAL_S_RET',
    'Meta Mensal Serviços $': 'SERV_META_TOT',
    'Valor Meta Eficiência Serviços': 'SERV_META_ACU',
    'Valor Realizado Eficiência Serviços': 'SERV_REAL',
    'Meta Mensal \nCDC $': 'CDC_META_TOT',
    'Valor Meta Participação CDC': 'CDC_META_ACU',
    'Valor Realizado Participação CDC': 'CDC_REAL',
    'Meta Mensal Móveis': 'MOVEIS_META_TOT',
    'Meta Mensal Eletro-Portateis': 'PORT_META_TOT',
    'Meta\nEletro Portátil': 'PORT_META_ACU',
    'Realizado\nEletro Portátil ': 'PORT_REAL',
    'Meta de Cartões': 'CARTAO_META_ACU',
    'Cartões Novos Realizados': 'CARTAO_REAL',
    'Meta Mensal \nCartões': 'CARTAO_META_TOT',
    'Meta NPS': 'NPS_META_TOT',
    'Realizado NPS': 'NPS_REAL'
}

df_loja = pd.read_excel('../EVVA/inputs/ad_hoc/Apuração RV Gerentes - Mensal_{}.xlsx'.format(DT_TODAY_FILE), sheet_name='Apuração Preliminar', skiprows=1)
df_piloto = pd.read_excel('../EVVA/inputs/ad_hoc/premiacao_diaria_piloto/Mod. de Premiação - Perfis e Portes de Loja v07_MAR-2019.xlsx', sheet_name='BD FILIAIS')
df_esp = pd.read_excel('../EVVA/inputs/de_paras/espelhamento.xlsx', sheet_name='Espelhamento')
df_loja.drop(columns = [col for col in df_loja if 'Unnamed:' in col], inplace = True)

# Filtra somente as colunas relevantes e as renomeia
df_loja = df_loja[list(rename_dict.keys())].rename(columns = rename_dict)
df_rot = pd.read_csv('../EVVA/inputs/de_paras/roteirizacao.csv', encoding='latin-1')
df_loja = pd.merge(df_loja,df_rot[['CD_FIL','CD_FUN_GER','NOME_GERENTE_LOJA']],on='CD_FIL',how='left')
df_piloto = df_piloto.rename(columns = {'Filial':'CD_FIL'})
df_loja = pd.merge(df_piloto,df_loja, on = 'CD_FIL', how = 'left')
df_loja = df_loja[~df_loja['CD_FUN_GER'].isnull()].reset_index().drop(columns = 'index')
df_loja['NOME_GERENTE_LOJA'] = df_loja['NOME_GERENTE_LOJA'].apply(lambda x: x.split()[0].capitalize())
df_loja['CD_FUN_GER'] = df_loja['CD_FUN_GER'].astype(int).astype(str)
df_loja['ICM_CDC'] = df_loja['ICM_CDC'].fillna(0)
df_loja['DT_NPS'] = df_loja['DT_NPS'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])
df_loja['DT_CART'] = df_loja['DT_CART'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])
df_loja.columns
df_loja['message'] = ''

for loja in df_loja.itertuples():
    format_dict = {
        'nome': loja.NOME_GERENTE_LOJA,
        'data': REF_DATE,
        'data_nps': loja.DT_NPS,
        'prem_loja': locale.format("%.0f", loja.PREM_TOT, True),
        'prem_merc_loja': locale.format("%.0f", loja.PREM_MERC, True),
        'prem_serv_loja': locale.format("%.0f", loja.PREM_SERV, True),
        'prem_cdc_loja': locale.format("%.0f", loja.PREM_CDC, True),
        'prem_mov': locale.format("%.0f", loja.PREM_MOV, True),
        'prem_port': locale.format("%.0f", loja.PREM_PORT, True),
        'prem_cart': locale.format("%.0f", loja.PREM_CART, True),
        'prem_nps': locale.format("%.0f", loja.PREM_NPS, True),
        'emoji_merc_loja': get_emoji(loja.ICM_MERC),
        'emoji_serv_loja': get_emoji(loja.ICM_SERV),
        'emoji_cdc_loja': get_emoji(loja.ICM_CDC),
        'emoji_mov': get_emoji(loja.ICM_MOV),
        'emoji_port': get_emoji(loja.ICM_PORT),
        'emoji_cart': get_emoji(loja.ICM_CART),
        'emoji_nps': get_emoji_nps(loja.ICM_NPS),
        'cump_merc_loja': int(round(loja.ICM_MERC * 100,3)),
        'cump_serv_loja': int(round(loja.ICM_SERV * 100,3)),
        'cump_cdc_loja': int(round(loja.ICM_CDC * 100,3)),
        'cump_mov': int(round(loja.ICM_MOV * 100,3)),
        'cump_port': int(round(loja.ICM_PORT * 100,3)),
        'cump_cart': int(round(loja.ICM_CART * 100,3)),
        'cump_nps': int(round(loja.ICM_NPS * 100,3)),
        'emoji_fam1': get_emoji_fam(loja.ICM_FAM1),
        'emoji_fam2': get_emoji_fam(loja.ICM_FAM2),
        'emoji_fam3': get_emoji_fam(loja.ICM_FAM3),
        'emoji_fam4': get_emoji_fam(loja.ICM_FAM4),
        'emoji_fam5': get_emoji_fam(loja.ICM_FAM5),
        'cump_fam1': int(round(loja.ICM_FAM1 * 100,3)),
        'cump_fam2': int(round(loja.ICM_FAM2 * 100,3)),
        'cump_fam3': int(round(loja.ICM_FAM3 * 100,3)),
        'cump_fam4': int(round(loja.ICM_FAM4 * 100,3)),
        'cump_fam5': int(round(loja.ICM_FAM5 * 100,3)),
        'data_cart': loja.DT_CART,
        'data_NPS': loja.DT_NPS,
        'criterio_merc': loja.CRITERIO_MERC

    }

    if loja.FLAG_PRQ_FAM != 'ok':
        format_dict['emoji_serv_loja'] = '❌'

    msg = TEMPLATE.format(**format_dict)

    if loja.PESO_CDC == 0:
        msg = msg.replace('❌ CDC: 0% ➡️ 💰R$0\n','')

    if loja.PESO_CART == 0:
        msg = msg.replace('❌ Cartões: 0% ➡️ 💰R$0\n','')

    if loja.PESO_MOV == 0:
        msg = msg.replace('❌ Móveis: 0% ➡️ 💰R$0\n','')

    msg = msg.replace('💰R$0','-')
    df_loja.at[loja.Index,'message'] = msg.rstrip()

porte_loja = re.compile(r'PORTE ')

df_loja['PORTE_NUMBER'] = df_loja['PORTE COM RETIRA'].apply(lambda x: re.sub(porte_loja,'',x))
df_loja.PORT_META_ACU = df_loja.PORT_META_ACU.fillna(0)
df_loja['CD_FUN_GER'] = df_loja.CD_FUN_GER.astype(int) + 2100000000
df_loja['url'] = ''

for fun in df_loja.itertuples():

    format_dict = {'cd_fun': int(fun.CD_FUN_GER),
        'cd_fil': int(fun.CD_FIL),
        'fil_porte': int(fun.PORTE_NUMBER),
        'fil_perfil': int(fun.TIPO_META),
        'serv_real': int(fun.SERV_REAL),
        'serv_meta_tot': int(fun.SERV_META_TOT),
        'serv_meta_acu': int(fun.SERV_META_ACU),
        'cdc_real': int(fun.CDC_REAL),
        'cdc_meta_tot': int(fun.CDC_META_TOT),
        'cdc_meta_acu': int(fun.CDC_META_ACU),
        'moveis_real': int(fun.MOVEIS_REAL_S_RET),
        'moveis_meta_tot': int(fun.MOVEIS_META_TOT),
        'moveis_meta_acu': int(fun.MOVEIS_META_ACU_S_RET),
        'port_real': int(fun.PORT_REAL),
        'port_meta_tot': int(fun.PORT_META_TOT),
        'port_meta_acu': int(fun.PORT_META_ACU),
        'cartao_real': int(fun.CARTAO_REAL),
        'cartao_meta_tot': int(fun.CARTAO_META_TOT),
        'cartao_meta_acu': int(fun.CARTAO_META_ACU),
        'nps_real': int(fun.NPS_REAL),
        'nps_meta_tot': int(fun.NPS_META_TOT),
        'dia': int(DT_DIA),
        'mes': int(DT_MES)
    }

    if fun.FLAG_PRQ_FAM == 'ok':
        format_dict['fam_serv'] = 1
    else:
        format_dict['fam_serv'] = 0

    if fun.CRITERIO_MERC == 'Sem Retira':
        format_dict['merc_real'] = int(fun.MOVEIS_REAL_S_RET + fun.PORT_REAL_S_RET)
        format_dict['merc_meta_tot'] = int(fun.MERC_META_TOT_S_RET)
        format_dict['merc_meta_acu'] = int(fun.MOVEIS_META_ACU_S_RET + fun.PORT_META_ACU_S_RET)
    else:
        format_dict['merc_real'] = int(fun.MERC_REAL)
        format_dict['merc_meta_tot'] = int(fun.MERC_META_TOT)
        format_dict['merc_meta_acu'] = int(fun.MERC_META_ACU)

    gerar_imagem_glm(**format_dict)

    gc.collect()
