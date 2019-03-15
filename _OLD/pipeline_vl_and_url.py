import pandas as pd
import numpy as np
import locale
import datetime
from random import randint
import re

pd.set_option('display.max_columns', None)

## Prêmio Líder Categoria

# Template da primeira metade do extrato do VL (Prêmio Líder Categoria)
TEMPLATE_CATEG = """
Oi {nome}, Olha como está a PROJEÇÃO dos seus PRÊMIOS de liderança baseado no resultado das suas categorias e da loja (até {data}):

💰LÍDER CATEG. PROJETADO: R${prem_tot}
 {emoji_merc} Merc: {cump_merc:.0f}% ➡️ 💰R${prem_merc}
 {emoji_serv} Serv: {cump_serv:.0f}% ➡️ 💰R${prem_serv}
 {emoji_cdc} CDC: {cump_cdc:.0f}% ➡️ 💰R${prem_cdc}
"""

# Template da segunda metade do extrato do VL (Prêmio Líder Loja)
TEMPLATE_LOJA = """

💰LÍDER LOJA PROJETADO: R${prem_loja}
 {emoji_merc_loja} Merc: {cump_merc_loja:.0f}% ➡️ 💰R${prem_merc_loja}
 ({criterio_merc})
 {emoji_serv_loja} Serv*: {cump_serv_loja:.0f}% ➡️ 💰R${prem_serv_loja}
 {emoji_cdc_loja} CDC: {cump_cdc_loja:.0f}% ➡️ 💰R${prem_cdc_loja}
 {emoji_mov} Móveis: {cump_mov:.0f}% ➡️ 💰R${prem_mov}
 {emoji_port} Portáteis: {cump_port:.0f}% ➡️ 💰R${prem_port}
 {emoji_cart} Cartões: {cump_cart:.0f}% ➡️ 💰R${prem_cart}
 (em {data_cart})
 {emoji_nps} NPS: {cump_nps:.0f}% ➡️ 💰R${prem_nps}
 (em {data_NPS})

"""

TEMPLATE_FAMILIA = """

*Olha como estão as Famílias de Serviços (pré-req 70%):
 {emoji_fam1} Família 1: {cump_fam1:.0f}%
 {emoji_fam2} Família 2: {cump_fam2:.0f}%
 {emoji_fam3} Família 3: {cump_fam3:.0f}%
 {emoji_fam4} Família 4: {cump_fam4:.0f}%
 {emoji_fam5} Família 5: {cump_fam5:.0f}%
"""

TEMPLATE_URL_CATEG = "https://bk9jvk64kh.execute-api.us-east-1.amazonaws.com/dev/vendedorlider/grafico_categ?cd_fun={cd_fun}&cd_fil={cd_fil}&merc_real={merc_real}&merc_meta_tot={merc_meta_tot}&merc_meta_acu={merc_meta_acu}&serv_real={serv_real}&serv_meta_tot={serv_meta_tot}&serv_meta_acu={serv_meta_acu}&cdc_real={cdc_real}&cdc_meta_tot={cdc_meta_tot}&cdc_meta_acu={cdc_meta_acu}&dia={dia}&mes={mes}"

TEMPLATE_URL_LOJA = "https://bk9jvk64kh.execute-api.us-east-1.amazonaws.com/dev/vendedorlider/grafico_loja?cd_fun={cd_fun}&cd_fil={cd_fil}&fil_porte={fil_porte}&fil_perfil={fil_perfil}&merc_real={merc_real}&merc_meta_tot={merc_meta_tot}&merc_meta_acu={merc_meta_acu}&serv_real={serv_real}&serv_meta_tot={serv_meta_tot}&serv_meta_acu={serv_meta_acu}&cdc_real={cdc_real}&cdc_meta_tot={cdc_meta_tot}&cdc_meta_acu={cdc_meta_acu}&moveis_real={moveis_real}&moveis_meta_tot={moveis_meta_tot}&moveis_meta_acu={moveis_meta_acu}&port_real={port_real}&port_meta_tot={port_meta_tot}&port_meta_acu={port_meta_acu}&cartao_real={cartao_real}&cartao_meta_tot={cartao_meta_tot}&cartao_meta_acu={cartao_meta_acu}&fam_serv={fam_serv}&nps_real={nps_real}&nps_meta_tot={nps_meta_tot}&dia={dia}&mes={mes}"

# Definição do locale para utilizar formatação com separador de milhar como '.'
locale.setlocale(locale.LC_ALL, 'Portuguese')

DT_TODAY = datetime.datetime.today()

DT_TODAY_FILE = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%Y.%m.%d')

DT_DIA = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%d')

DT_MES = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%m')

DT_TODAY_FILE_2 = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%Y%m%d')

DATE_FILE = DT_TODAY.strftime('%Y%m%d')

### Cleasing Líder Categoria

# Dicionário das colunas relevantes e o de-para de nomenclatura
rename_dict = {
   'DtRef': 'DT_REF', 
   'Matrícula': 'CD_FUN', 
   'Funcionário': 'NOME', 
   'Cod Estab': 'CD_FIL',
   'Target': 'TARGET',
   'Peso\nVenda Mercantil Categoria': 'PESO_MERC', 
   'Target \nVenda Mercantil Categoria': 'TARGET_MERC',
   'Meta \nVenda Mercantil\nCategoria': 'META_MERC',
   'Realizado\nVenda Mercantil\nCategoria': 'REAL_MERC',
   '% Cumpr \nVenda Mercantil\nCategoria': 'CUMP_MERC',
   'Faixas de Atingimento\nVenda Mercantil\nCategoria': 'FAIXA_MERC',
   'Acelerador \nVenda Mercantil\nCategoria': 'ACEL_MERC',
   'Peso\nEfic Serviços\nCategoria': 'PESO_SERV',
   'Target \nEfic Serviços\nCategoria': 'TARGET_SERV',
   'Meta \nEfic Serviços $\nCategoria': 'META_SERV',
   'Realizado\nEfic Serviços $\nCategoria': 'REAL_SERV',
   '% Cumpr \nEfic Serviços $\nCategoria': 'CUMP_SERV',
   'Faixas de Atingimento\nEfic Serviços\nCategoria': 'FAIXA_SERV',
   'Acelerador \nEfic Serviços\nCategoria': 'ACEL_SERV',
   'Peso\nCDC\nCategoria': 'PESO_CDC',
   'Target \nCDC\nCategoria': 'TARGET_CDC',
   'Meta \nCDC $\nCategoria': 'META_CDC',
   'Realizado\nCDC $\nCategoria': 'REAL_CDC',
   '% Cumpr \nCDC $\nCategoria': 'CUMP_CDC',
   'Faixas de Atingimento\nCDC\nCategoria': 'FAIXA_CDC',
   'Acelerador \nCDC\nCategoria': 'ACEL_CDC',
   'Valor Prêmio\nVenda Mercantil\nCategoria.1': 'PREM_MERC',
   'Valor Prêmio\nEfic Serviços\nCategoria.1': 'PREM_SERV',
   'Valor Prêmio\nCDC\nCategoria.1': 'PREM_CDC', 
   'Valor Prêmio\nTotal\nCategoria': 'PREM_TOT',
    'Meta Mensal\nVenda Mercantil\nCategoria': 'MERC_META_TOT_CATEG',
    'Meta Mensal\nEfic Serviços $\nCategoria': 'SERV_META_TOT_CATEG',
    'Meta Mensal\nCDC $\nCategoria': 'CDC_META_TOT_CATEG'
}

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

# Função para acertar o emoji pra cada indicador
def get_emoji(cump):
    if cump >= 100:
        return '✅'
    elif cump >= 90:
        return '⚠'
    else:
        return '❌'

# Função para acertar o emoji para o NPS
def get_emoji_nps(cump):
    if cump >= 100:
        return '✅'
    else:
        return '❌'

# Função para acertar o emoji para os indicadores de família de serviços
def get_emoji_fam(cump):
    if cump >= 100:
        return '✅'
    elif cump >= 70:
        return '⚠'
    else:
        return '❌'

# Função para ajustar a data
def fix_date(timestamp):
    return str(timestamp.day) + '/' + month_dict[timestamp.month]

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


# Lê a base do Piloto do VL e retira colunas inúteis
df_categ = pd.read_excel('./inputs/ad_hoc/VENDEDORLIDER_Categoria_{}.xlsx'.format(DT_TODAY_FILE_2), skiprows=1)
df_categ.drop(columns = [col for col in df_categ if type(col) == int], inplace = True)
df_categ.drop(columns = [col for col in df_categ if 'Unnamed:' in col], inplace = True)

list(df_categ)

# Filtra somente as colunas relevantes e as renomeia
df_categ = df_categ[list(rename_dict.keys())].rename(columns = rename_dict)

df_categ[[col for col in df_categ if 'CUMP' in col]] = df_categ[[col for col in df_categ if 'CUMP' in col]] * 100

# Ajusta as colunas de Nome e Data
df_categ['NOME'] = df_categ['NOME'].apply(lambda x: x.split()[0].capitalize())
df_categ['DT_REF'] = df_categ['DT_REF'].apply(fix_date)

### Cleasing Líder Loja

rename_dict2 = {
     'Estabelecimento': 'CD_FIL',
#      'Regional': 'CD_REG',
#      'Diretoria': 'CD_DIR',
     '% Eficiência Serviços Valor': 'ICM_SERV',
     '% Participação CDC Valor': 'ICM_CDC',
     '% Família 1 (Garantia Eletro + Garantia Moveis)': 'ICM_FAM1',
     '% Família 2 (VPP + Prot Financeira + Tecnico + Saúde Premiada)': 'ICM_FAM2',
     '% Família 3  (Residencial + Multiassistência)': 'ICM_FAM3',
     '% Família 4 (Fique Seguro)': 'ICM_FAM4',
#      '% Família 5 (Portateis)': 'ICM_FAM5',
     '% Planos': 'ICM_FAM5',
     'PORTE': 'PORTE',
#      'TARGET MENSAL': 'TARGET',
     'TIPO PAINEL': 'TIPO_META',
     'ICM Mercantil Final': 'ICM_MERC',
#      'Faixa Mercantil': 'FAIXA_MERC',
     'Peso Mercantil': 'PESO_MERC',
     'Payout Mercantil': 'PAY_MERC',
#      'Prêmio Mercantil': 'PREM_MERC',
#      'Pré Requisito Famílias': 'N_PRQ_FAM',
     'Cumpr. Pré Requisito': 'FLAG_PRQ_FAM',
     'ICM Serviços Final': 'ICM_SERV_OFC',
#      'Faixa Serviços': 'FAIXA_SERV',
     'Peso Serviços': 'PESO_SERV',
     'Payout Serviços': 'PAY_SERV',
#      'Prêmio Serviços': 'PREM_SERV',
#      'Faixa CDC': 'FAIXA_CDC',
     'Peso CDC': 'PESO_CDC',
     'Payout CDC': 'PAY_CDC',
#      'Prêmio CDC': 'PREM_CDC',
     'ICM Móveis': 'ICM_MOV',
#      'Faixa Móveis': 'FAIXA_MOV',
     'Peso Móveis': 'PESO_MOV',
     'Payout Móveis': 'PAY_MOV',
#      'Prêmio Móveis': 'PREM_MOV',
     'ICM Portáteis': 'ICM_PORT',
#      'Faixa Portateis': 'FAIXA_PORT',
     'Peso Portatéis': 'PESO_PORT',
     'Payout Portáteis': 'PAY_PORT',
#      'Prêmio Portáteis': 'PREM_PORT',
     'ICM Cartões': 'ICM_CART',
#      'Faixa Cartões': 'FAIXA_CART',
     'Peso Cartões': 'PESO_CART',
     'Payout Cartões': 'PAY_CART',
#      'Prêmio Cartões': 'PREM_CART',
     'ICM NPS': 'ICM_NPS',
#      'Prêmio NPS': 'PREM_NPS',
#      'Prêmio TOTAL': 'PREM_TOT',
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

df_loja = pd.read_excel('./inputs/ad_hoc/Apuração RV Gerentes - Mensal_{}.xlsx'.format(DT_TODAY_FILE), sheet_name='Apuração Preliminar', skiprows=1)
df_loja.drop(columns = [col for col in df_loja if 'Unnamed:' in col], inplace = True)

# Filtra somente as colunas relevantes e as renomeia
df_loja = df_loja[list(rename_dict2.keys())].rename(columns = rename_dict2)

df_loja[[col for col in df_loja if 'ICM' in col]] = df_loja[[col for col in df_loja if 'ICM' in col]].replace('sem meta',0) * 100

ind_list = [col.split('_')[1] for col in df_loja if 'PESO' in col]

TARGET = 1200
#Calculando a premiação por indicador
for indicador in ind_list:
    df_loja['PREM_' + indicador] = df_loja['PAY_' + indicador] * df_loja['PESO_' + indicador] * TARGET

df_loja['PREM_NPS'] = (df_loja['ICM_NPS'] >= 100) * 120

df_loja['PREM_TOT'] = df_loja[[col for col in df_loja if 'PREM' in col]].sum(axis=1)

df_loja['ICM_CDC'] = df_loja['ICM_CDC'].fillna(0)

df_loja.FLAG_PRQ_FAM.unique()

df_loja['DT_NPS'] = df_loja['DT_NPS'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])

df_loja['DT_CART'] = df_loja['DT_CART'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])

### Merge para calcular o total da premiação (Categoria + Loja)

df_loja_TT = df_loja[['CD_FIL','PREM_TOT']]

df_loja_TT = df_loja_TT.rename(columns = {'PREM_TOT':'TOTAL_LIDER_LOJA'})

df_categ.columns

df_categ = pd.merge(df_categ,df_loja_TT, on = 'CD_FIL', how = 'left' )

df_categ['TT_PROJ'] = df_categ['TOTAL_LIDER_LOJA'] + df_categ['PREM_TOT']

df_categ['TT_PROJ'] = df_categ['TT_PROJ'].astype(float)

df_categ['TT_PROJ'] = df_categ['TT_PROJ'].apply(lambda x: locale.format("%.0f",x, True))

df_categ['msg_tt'] = ''
for vl in df_categ.itertuples():
    x = """
    
💰TOTAL CATEG. + LOJA: R${}""".format(vl.TT_PROJ).replace('R$0','-')
    
    df_categ.at[vl.Index,'msg_tt'] = x.rstrip()

print(df_categ['msg_tt'][5])

### Output MSG Líder Categoria

# Geração das mensagens
df_categ['message'] = ''

for vl in df_categ.itertuples():
    format_dict = {
        'nome': vl.NOME,
        'data': vl.DT_REF,
        'prem_tot': locale.format("%.0f", vl.PREM_TOT, True),
        'emoji_merc': get_emoji(int(vl.CUMP_MERC)),
        'cump_merc': int(vl.CUMP_MERC),
        'prem_merc': locale.format("%.0f", vl.PREM_MERC, True),
        'emoji_serv': get_emoji(int(vl.CUMP_SERV)),
        'cump_serv': int(vl.CUMP_SERV),
        'prem_serv': locale.format("%.0f", vl.PREM_SERV, True),
        'emoji_cdc': get_emoji(int(vl.CUMP_CDC)),
        'cump_cdc': int(vl.CUMP_CDC),
        'prem_cdc': locale.format("%.0f", vl.PREM_CDC, True)
    }
    
    msg = TEMPLATE_CATEG.format(**format_dict)
    
    if vl.PESO_CDC == 0:
        msg = msg.replace('❌ CDC: 0% ➡️ 💰R$0\n','')
        
    msg = msg.replace('💰R$0','-')
    msg = msg.replace('R$0','-')
    
    df_categ.at[vl.Index,'message'] = msg.rstrip()

df_categ['CD_FUN'] = df_categ.CD_FUN.astype(int) + 2100000000

df_categ['url1'] = ''
for fun in df_categ.itertuples():
    format_dict = {'cd_fun': fun.CD_FUN,
        'cd_fil': fun.CD_FIL,
        'merc_real': int(fun.REAL_MERC),
        'merc_meta_tot': int(fun.MERC_META_TOT_CATEG),
        'merc_meta_acu': int(fun.META_MERC),
        'serv_real': int(fun.REAL_SERV),
        'serv_meta_tot': int(fun.SERV_META_TOT_CATEG),
        'serv_meta_acu': int(fun.META_SERV),
        'cdc_real': int(fun.REAL_CDC),
        'cdc_meta_tot': int(fun.CDC_META_TOT_CATEG),
        'cdc_meta_acu': int(fun.META_CDC),
        'dia': DT_DIA,
        'mes': DT_MES
    }
        
    msg_url = TEMPLATE_URL_CATEG.format(**format_dict)
    
    df_categ.at[fun.Index,'url1'] = msg_url.rstrip()

print(df_categ.loc[randint(0,df_categ.shape[0] - 1),'url1'])

print(df_categ.loc[randint(0,df_categ.shape[0] - 1),'message'])

### Output MSG Líder Loja

df_loja['msg_loja'] = ''

for loja in df_loja.itertuples():
    format_dict = {
        'prem_loja': locale.format("%.0f", loja.PREM_TOT, True),
        'prem_merc_loja': locale.format("%.0f", loja.PREM_MERC, True),
        'prem_serv_loja': locale.format("%.0f", loja.PREM_SERV, True),
        'prem_cdc_loja': locale.format("%.0f", loja.PREM_CDC, True),
        'prem_mov': locale.format("%.0f", loja.PREM_MOV, True),
        'prem_port': locale.format("%.0f", loja.PREM_PORT, True),
        'prem_cart': locale.format("%.0f", loja.PREM_CART, True),
        'prem_nps': locale.format("%.0f", loja.PREM_NPS, True),
        'emoji_merc_loja': get_emoji(int(loja.ICM_MERC)),
        'emoji_serv_loja': get_emoji(int(loja.ICM_SERV)),
        'emoji_cdc_loja': get_emoji(int(loja.ICM_CDC)),
        'emoji_mov': get_emoji(int(loja.ICM_MOV)),
        'emoji_port': get_emoji(int(loja.ICM_PORT)),
        'emoji_cart': get_emoji(int(loja.ICM_CART)),
        'emoji_nps': get_emoji_nps(int(loja.ICM_NPS)),
        'cump_merc_loja': int(round(loja.ICM_MERC,3)),
        'cump_serv_loja': int(round(loja.ICM_SERV,3)),
        'cump_cdc_loja': int(round(loja.ICM_CDC,3)),
        'cump_mov': int(round(loja.ICM_MOV,3)),
        'cump_port': int(round(loja.ICM_PORT,3)),
        'cump_cart': int(round(loja.ICM_CART,3)),
        'cump_nps': int(round(loja.ICM_NPS,3)),
        'emoji_fam1': get_emoji_fam(int(loja.ICM_FAM1)),
        'emoji_fam2': get_emoji_fam(int(loja.ICM_FAM2)),
        'emoji_fam3': get_emoji_fam(int(loja.ICM_FAM3)),
        'emoji_fam4': get_emoji_fam(int(loja.ICM_FAM4)),
        'emoji_fam5': get_emoji_fam(int(loja.ICM_FAM5)),
        'cump_fam1': int(round(loja.ICM_FAM1,3)),
        'cump_fam2': int(round(loja.ICM_FAM2,3)),
        'cump_fam3': int(round(loja.ICM_FAM3,3)),
        'cump_fam4': int(round(loja.ICM_FAM4,3)),
        'cump_fam5': int(round(loja.ICM_FAM5,3)),
        'data_cart': loja.DT_CART,
        'data_NPS': loja.DT_NPS,
        'criterio_merc': loja.CRITERIO_MERC
        
        
    }
    
    if loja.FLAG_PRQ_FAM != 'ok':
        format_dict['emoji_serv_loja'] = '❌'
    
    msg = TEMPLATE_LOJA.format(**format_dict)
    
    if loja.PESO_CDC == 0:
        msg = msg.replace('❌ CDC: 0% ➡️ 💰R$0\n','')
        
    if loja.PESO_CART == 0:
        msg = msg.replace('❌ Cartões: 0% ➡️ 💰R$0\n','')
        
    if loja.PESO_MOV == 0:
        msg = msg.replace('❌ Móveis: 0% ➡️ 💰R$0\n','')
    
    msg = msg.replace('💰R$0','-')
    msg = msg.replace('R$0','-')
    
    df_loja.at[loja.Index,'msg_loja'] = msg.rstrip()   

df_loja['msg_familia'] = ''

for loja in df_loja.itertuples():
    format_dict = {
        'emoji_fam1': get_emoji_fam(int(loja.ICM_FAM1)),
        'emoji_fam2': get_emoji_fam(int(loja.ICM_FAM2)),
        'emoji_fam3': get_emoji_fam(int(loja.ICM_FAM3)),
        'emoji_fam4': get_emoji_fam(int(loja.ICM_FAM4)),
        'emoji_fam5': get_emoji_fam(int(loja.ICM_FAM5)),
        'cump_fam1': int(round(loja.ICM_FAM1,3)),
        'cump_fam2': int(round(loja.ICM_FAM2,3)),
        'cump_fam3': int(round(loja.ICM_FAM3,3)),
        'cump_fam4': int(round(loja.ICM_FAM4,3)),
        'cump_fam5': int(round(loja.ICM_FAM5,3)),
    }
    
    msg = TEMPLATE_FAMILIA.format(**format_dict)
    
    df_loja.at[loja.Index,'msg_familia'] = msg.rstrip() 

df_loja = pd.merge(df_categ,df_loja, on='CD_FIL', how= 'left')

porte_loja = re.compile(r'PORTE ')

df_loja['PORTE_NUMBER'] = df_loja['PORTE'].apply(lambda x: re.sub(porte_loja,'',x))

df_loja.PORT_META_ACU = df_loja.PORT_META_ACU.fillna(0)

# df_loja['CD_FUN_GER'] = df_loja.CD_FUN.astype(int) + 2100000000

df_loja['url2'] = ''

for fun in df_loja.itertuples():
    format_dict = {'cd_fun': fun.CD_FUN,
        'cd_fil': fun.CD_FIL,
        'fil_porte': fun.PORTE_NUMBER,
        'fil_perfil': fun.TIPO_META,
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
        'dia': DT_DIA,
        'mes': DT_MES
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
        
    
    msg_url = TEMPLATE_URL_LOJA.format(**format_dict)
    
    df_loja.at[fun.Index,'url2'] = msg_url.rstrip()

print(df_loja.loc[randint(0,df_loja.shape[0] - 1),'url2'])

print(df_loja.loc[randint(0,df_categ.shape[0] - 1),'msg_loja'])

### Output Final

df_print = df_loja.copy()

# df_print = df_categ[['CD_FUN','message','msg_tt','CD_FIL']].merge(df_loja[['CD_FIL','msg_loja','msg_familia']], on='CD_FIL')

df_print['m5'] = df_print['message'] + df_print['msg_loja'] + df_print['msg_tt'] + df_print['msg_familia']

df_print = df_print.drop(columns=['CD_FIL','msg_loja']).rename(columns={'CD_FUN':'username'})

df_print['username'] = df_print['username'].astype(str)

print(df_print.loc[randint(0,df_print.shape[0] - 1),'m5'])

df_categ.shape

df_print = df_print[['username','url1','url2','m5']]

df_esp = pd.read_excel('./inputs/de_paras/espelhamento.xlsx', sheet_name ='Espelhamento')

df_print = get_espelhamento(df_print,df_esp,'VL')

df_print.head()

df_print['flow'] = 'strings_img2x_strings'

df_print = df_print[['username','flow','url1','url2','m5']]

df_print.to_csv('./outputs/to_be_sent/{}/vendedor_lider_{}.csv'.format(DATE_FILE,DATE_FILE), index=False)