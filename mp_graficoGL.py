import multiprocessing
import datetime
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import locale
from multiprocessing.dummy import Pool

perc_ating = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 105, 110, 115, 120, 125, 130]

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

DT_TODAY = datetime.datetime.today()#.replace(day = 12)
DT_TODAY_FILE = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%Y.%m.%d')
DT_DIA = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%d')
DT_MES = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%m')
DATE_FILE = DT_TODAY.strftime('%Y%m%d')
REF_DATE = DT_TODAY.replace(day = DT_TODAY.day - 1 ).strftime('%d/') + month_dict[DT_TODAY.month]


rename_dict = {
        'Estabelecimento': 'CD_FIL',
        '% Eficiência Serviços Valor': 'ICM_SERV',
        '% Participação CDC Valor': 'ICM_CDC',
        '% Família 1 (Garantia Eletro + Garantia Moveis)': 'ICM_FAM1',
        '% Família 2 (VPP + Prot Financeira + Tecnico + Saúde Premiada)': 'ICM_FAM2',
        '% Família 3  (Residencial + Multiassistência)': 'ICM_FAM3',
        '% Família 4 (Fique Seguro)': 'ICM_FAM4',
        '% Planos': 'ICM_FAM5',
        'PORTE': 'PORTE',
        'TARGET MENSAL': 'TARGET',
        'TIPO PAINEL': 'TIPO_META',
        'ICM Mercantil Final': 'ICM_MERC',
        'Peso Mercantil': 'PESO_MERC',
        'Payout Mercantil': 'PAY_MERC',
        'Prêmio Mercantil': 'PREM_MERC',
        'Cumpr. Pré Requisito': 'FLAG_PRQ_FAM',
        'ICM Serviços Final': 'ICM_SERV_OFC',
        'Peso Serviços': 'PESO_SERV',
        'Payout Serviços': 'PAY_SERV',
        'Prêmio Serviços': 'PREM_SERV',
        'Peso CDC': 'PESO_CDC',
        'Payout CDC': 'PAY_CDC',
        'Prêmio CDC': 'PREM_CDC',
        'ICM Móveis': 'ICM_MOV',
        'Peso Móveis': 'PESO_MOV',
        'Payout Móveis': 'PAY_MOV',
        'Prêmio Móveis': 'PREM_MOV',
        'ICM Portáteis': 'ICM_PORT',
        'Peso Portatéis': 'PESO_PORT',
        'Payout Portáteis': 'PAY_PORT',
        'Prêmio Portáteis': 'PREM_PORT',
        'ICM Cartões': 'ICM_CART',
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


def mp_handler(df_loja):
    for fun in df_loja.itertuples():
        p = Pool(1)
        p.map(gerar_imagem_glm, [fun])
        p.close()
        p.join()


def get_ylabels(meta_total):
    aux = perc_ating.copy()
    for i, perc in enumerate(aux):
        aux[i] = 'R$ ' + locale.format('%.0f', int(perc * meta_total / 100), True)

    return aux


def get_ylabels2(meta_total):
    aux = perc_ating.copy()
    for i, perc in enumerate(aux):
        aux[i] = locale.format('%.0f', int(perc * meta_total / 100), True)

    return aux


def gerar_imagem_glm(fun):
    
    cd_fun = int(fun.CD_FUN_GER)
    cd_fil = int(fun.CD_FIL)
    fil_porte = int(fun.PORTE_NUMBER)
    fil_perfil = int(fun.TIPO_META)
    
    if fun.CRITERIO_MERC == 'Sem Retira':
        merc_real = int(fun.MOVEIS_REAL_S_RET + fun.PORT_REAL_S_RET)
        merc_meta_tot = int(fun.MERC_META_TOT_S_RET)
        merc_meta_acu = int(fun.MOVEIS_META_ACU_S_RET + fun.PORT_META_ACU_S_RET)
    else:
        merc_real = int(fun.MERC_REAL)
        merc_meta_tot = int(fun.MERC_META_TOT)
        merc_meta_acu = int(fun.MERC_META_ACU)


    serv_real = int(fun.SERV_REAL)
    serv_meta_tot = int(fun.SERV_META_TOT)
    serv_meta_acu = int(fun.SERV_META_ACU)
    cdc_real = int(fun.CDC_REAL)
    cdc_meta_tot = int(fun.CDC_META_TOT)
    cdc_meta_acu = int(fun.CDC_META_ACU)
    moveis_real = int(fun.MOVEIS_REAL_S_RET)
    moveis_meta_tot = int(fun.MOVEIS_META_TOT)
    moveis_meta_acu = int(fun.MOVEIS_META_ACU_S_RET)
    port_real = int(fun.PORT_REAL)
    port_meta_tot = int(fun.PORT_META_TOT)
    port_meta_acu = int(fun.PORT_META_ACU)
    cartao_real = int(fun.CARTAO_REAL)
    cartao_meta_tot = int(fun.CARTAO_META_TOT)
    cartao_meta_acu = int(fun.CARTAO_META_ACU)

    if fun.FLAG_PRQ_FAM == 'ok':
        fam_serv = 1
    else:
        fam_serv = 0

    nps_real = int(fun.NPS_REAL)
    nps_meta_tot = int(fun.NPS_META_TOT)
    dia = int(DT_DIA)
    mes = int(DT_MES)
    
    
    locale.setlocale(locale.LC_ALL, 'German')
    # CRIAÇÃO DE ATINGIMENTOS
    # Mercantil
    merc_ating_real = merc_real / merc_meta_tot
    merc_ating_ritmo = merc_meta_acu / merc_meta_tot
    merc_ating_acu = merc_real / merc_meta_acu

    # Serviços
    serv_ating_real = serv_real / serv_meta_tot
    serv_ating_ritmo = serv_meta_acu / serv_meta_tot
    serv_ating_acu = serv_real / serv_meta_acu

    # CDC
    if str(fil_perfil)[2] == '1':
        cdc_ating_real = cdc_real / cdc_meta_tot
        cdc_ating_ritmo = cdc_meta_acu / cdc_meta_tot
        cdc_ating_acu = cdc_real / cdc_meta_acu
    else:
        cdc_ating_real = 0
        cdc_ating_ritmo = 0
        cdc_ating_acu = 0

    #Móveis
    if str(fil_perfil)[3] == '1':
        moveis_ating_real = moveis_real / moveis_meta_tot
        moveis_ating_ritmo = moveis_meta_acu / moveis_meta_tot
        moveis_ating_acu = moveis_real / moveis_meta_acu
    else:
        moveis_ating_real = 0
        moveis_ating_ritmo = 0
        moveis_ating_acu = 0

    #Eletroportáteis
    if str(fil_perfil)[4] == '1':
        port_ating_real = port_real / port_meta_tot
        port_ating_ritmo = port_meta_acu / port_meta_tot
        port_ating_acu = port_real / port_meta_acu
    else:
        port_ating_real = 0
        port_ating_ritmo = 0
        port_ating_acu = 0

    #Cartão
    if str(fil_perfil)[5] == '1':
        cartao_ating_real = cartao_real / cartao_meta_tot
        cartao_ating_ritmo = cartao_meta_acu / cartao_meta_tot
        if cartao_meta_acu > 0:
            cartao_ating_acu = cartao_real / cartao_meta_acu
        else:
            cartao_ating_acu = 0
    else:
        cartao_ating_real = 0
        cartao_ating_ritmo = 0
        cartao_ating_acu = 0

    #NPS
    nps_ating_real = float(nps_real / nps_meta_tot)

    # COORDENADAS DO GRÁFICO P/ LABELS AUX

    # Labels Prêmio (e.g. R$ 100, R$ 200)
    ref_lab100_y = 0.67 # 0.658
    ref_lab100_x = 0.230 # 0.156
    # ref_lab100_x = 0.298 # 0.156
    ref_delta_y = 0.028 # 0.0315

    # Label "Meta de Venda" p/ eixo Y
    ref_labmeta_y = 0.87 # 0.878
    ref_labmeta_x = 0.175 # 0.052
    # ref_labmeta_x = 0.202 # 0.052

    # Label "Prêmio"
    ref_labprem_y = 0.87 # 0.875
    ref_labprem_x = 0.245 # 0.173
    # ref_labprem_x = 0.318 # 0.173

    #Label "Meta até"
    ref_labmetaate_x = 0.224

    #Label "Venda Realizada"
    ref_labvendareal_x = 0.16

    # Delta entre um gráfico e outro (eixo X)
    ref_delta_x = 0.121 # 0.327
    # ref_delta_x = 0.225 # 0.327


    # PARÂMETROS DE PREMIAÇÃO (Versão com e sem meta de CDC)
    prem_90 = 0.5
    prem_100 = 1
    prem_step = 0.1

    # DISTRIBUIÇÃO DO TARGET PELO PERFIL
    map_fil_porte_target = {1: 1650,
                            2: 1875,
                            3: 2400,
                            4: 3000,
                            5: 3750,
                            6: 4500}

    map_fil_perfil_dist_target = {111111: {'target_merc': 0.25, 'target_serv': 0.25, 'target_cdc': 0.20, 'target_moveis': 0.15, 'target_port': 0.10, 'target_cartao': 0.05},  # PERFIL A
                                  110111: {'target_merc': 0.30, 'target_serv': 0.30, 'target_cdc': 0.00, 'target_moveis': 0.15, 'target_port': 0.10, 'target_cartao': 0.15},  # PERFIL B
                                  111011: {'target_merc': 0.35, 'target_serv': 0.25, 'target_cdc': 0.20, 'target_moveis': 0.00, 'target_port': 0.15, 'target_cartao': 0.05},  # PERFIL C
                                  111110: {'target_merc': 0.30, 'target_serv': 0.25, 'target_cdc': 0.20, 'target_moveis': 0.15, 'target_port': 0.10, 'target_cartao': 0.00},  # PERFIL D
                                  110011: {'target_merc': 0.40, 'target_serv': 0.30, 'target_cdc': 0.00, 'target_moveis': 0.00, 'target_port': 0.15, 'target_cartao': 0.15},  # PERFIL E
                                  110110: {'target_merc': 0.35, 'target_serv': 0.40, 'target_cdc': 0.00, 'target_moveis': 0.15, 'target_port': 0.10, 'target_cartao': 0.00},  # PERFIL F
                                  111001: {'target_merc': 0.50, 'target_serv': 0.25, 'target_cdc': 0.20, 'target_moveis': 0.00, 'target_port': 0.00, 'target_cartao': 0.05},  # PERFIL G
                                  111010: {'target_merc': 0.35, 'target_serv': 0.30, 'target_cdc': 0.20, 'target_moveis': 0.00, 'target_port': 0.15, 'target_cartao': 0.00},  # PERFIL H
                                  110001: {'target_merc': 0.50, 'target_serv': 0.35, 'target_cdc': 0.00, 'target_moveis': 0.00, 'target_port': 0.00, 'target_cartao': 0.15},  # PERFIL I
                                  110010: {'target_merc': 0.45, 'target_serv': 0.40, 'target_cdc': 0.00, 'target_moveis': 0.00, 'target_port': 0.15, 'target_cartao': 0.00},  # PERFIL J
                                  110000: {'target_merc': 0.60, 'target_serv': 0.40, 'target_cdc': 0.00, 'target_moveis': 0.00, 'target_port': 0.00, 'target_cartao': 0.00},  # PERFIL K
                                  111000: {'target_merc': 0.40, 'target_serv': 0.35, 'target_cdc': 0.25, 'target_moveis': 0.00, 'target_port': 0.00, 'target_cartao': 0.00}}  # PERFIL P

    map_fil_porte_prem_nps = {1: 165,
                              2: 190,
                              3: 240,
                              4: 300,
                              5: 375,
                              6: 450}

    data = '{:02d}/{:02d}'.format(dia,mes)

    # figsize=(12.8, 7.2), dpi = 80
    fig = plt.figure(figsize=(20, 7.2), dpi = 80)

    # Configuração do Grid
    gs0 = gridspec.GridSpec(1, 77, figure=fig)

    # Subplot com o Eixo dos atingimentos % (até 130%)
    ax1 = plt.Subplot(fig, gs0[:,0:7], frame_on = False)
    fig.add_subplot(ax1)

    # Subplot Mercantil
    merc = plt.Subplot(fig, gs0[:,7:17], frame_on = False)
    fig.add_subplot(merc)

    # Subplot Serviços
    serv = plt.Subplot(fig, gs0[:,19:29], frame_on = False)
    fig.add_subplot(serv)

    # Subplot CDC
    cdc = plt.Subplot(fig, gs0[:,31:41], frame_on = False)
    fig.add_subplot(cdc)

    # Subplot Móveis
    moveis = plt.Subplot(fig, gs0[:,43:53], frame_on = False)
    fig.add_subplot(moveis)

    # Subplot Eletroportáteis
    port = plt.Subplot(fig, gs0[:,55:65], frame_on = False)
    fig.add_subplot(port)

    # Subplot Cartões
    cartao = plt.Subplot(fig, gs0[:,67:77], frame_on = False)
    fig.add_subplot(cartao)

    width = [2,8]

    y_val = perc_ating

    ax1.set_yticks(y_val)
    ax1.set_yticklabels(map(lambda x: str(x) + '%', y_val), fontsize=12, weight='bold')
    ax1.set_xticks([])
    ax1.bar([1], [max(y_val)], width, color = ['#ffffff'], edgecolor = ['#ffffff'], linewidth = 0, align = 'edge')
    ax1.tick_params(axis='y', which='both', left=False)

    for tick in ax1.yaxis.get_major_ticks()[:8]:
        tick.label.set_color('white')

    for tick in ax1.yaxis.get_major_ticks()[10:16:2]:
        tick.label.set_color('lightgray')

    merc.set_yticks(y_val)
    merc.set_yticklabels(get_ylabels(merc_meta_tot), fontsize=11)
    merc.set_xticks([])

    serv.set_yticks(y_val)
    serv.set_yticklabels(get_ylabels(serv_meta_tot), fontsize=11)
    serv.set_xticks([])

    cdc.set_yticks(y_val)
    cdc.set_yticklabels(get_ylabels(cdc_meta_tot), fontsize=11)
    cdc.set_xticks([])

    moveis.set_yticks(y_val)
    moveis.set_yticklabels(get_ylabels(moveis_meta_tot), fontsize=11)
    moveis.set_xticks([])

    port.set_yticks(y_val)
    port.set_yticklabels(get_ylabels(port_meta_tot), fontsize=11)
    port.set_xticks([])

    cartao.set_yticks(y_val)
    cartao.set_yticklabels(get_ylabels2(cartao_meta_tot), fontsize=11)
    cartao.set_xticks([])

    # ------------------------------------------------ TARGET e PERFIL -----------------------------------------------------

    target = map_fil_porte_target[fil_porte]
    map_dist_target = map_fil_perfil_dist_target[fil_perfil]
    target_merc = map_dist_target['target_merc']
    target_serv = map_dist_target['target_serv']
    target_cdc = map_dist_target['target_cdc']
    target_moveis = map_dist_target['target_moveis']
    target_port = map_dist_target['target_port']
    target_cartao = map_dist_target['target_cartao']

    # ------------------------------------------------ MERCANTIL -----------------------------------------------------------

    p_cor = ['#ffffff'] # cores de preenchimento das barras em HEX https://xkcd.com/color/rgb/
    p_edcor = ['#929591'] # cores da borda das barras em HEX https://xkcd.com/color/rgb/
    p_lw = 1.2 # espessura das linhas
    p_ls = '--'

    for val in y_val[:7:-1]:
            merc.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    merc.bar([1,2], [min(merc_ating_real*100, 130),0], width, color = ['#bcecac'], edgecolor = ['#bcecac'], linewidth = 2.6, align = 'edge')

    props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='white')

    merc.set_title('Mercantil', fontsize=12, fontweight='bold', color='white', loc = 'left', bbox=props, pad = 30)

    merc.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
    merc.axhline(merc_ating_ritmo * 100, color='#3f9b0b', xmin = 0.05, xmax = 0.25, linewidth = 3)
    merc.tick_params(axis='y', which='both', left=False)

    # init = merc_prem_min + get_acelerador(serv_ating_acu, cdc_ating_acu, cdc_meta_tot)

    current_prize = min(max((round(merc_ating_real*100, 4) - 100)//5 + 1,0), 7)

    for i, val in enumerate(y_val[9:]):
        if (i + 1) == current_prize:
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#06470c'
        if i % 2 == 1:
            color2 = 'lightgray'

        fig.text(ref_lab100_x, ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_merc * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

    if (merc_ating_real*100 >= 90) and (merc_ating_real*100 <100):
        weight = 'bold'
        props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
        color2 = 'white'
    else:
        weight = 'normal'
        props2 = None
        color2 = '#06470c'
    fig.text(ref_lab100_x, ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_merc * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)

    fig.text(ref_labmeta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    for tick in merc.yaxis.get_major_ticks()[:8]:
        tick.label.set_color('white')

    for tick in merc.yaxis.get_major_ticks()[10:16:2]:
        tick.label.set_color('lightgray')

    merc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    if (merc_ating_ritmo >= 0.86) and (merc_ating_ritmo <= 0.9):
        fig.text(ref_labmetaate_x + 0* ref_delta_x, 0.12 + merc_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', merc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
    elif merc_ating_ritmo < 0.86:
        fig.text(ref_labmetaate_x + 0* ref_delta_x, 0.12 + merc_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', merc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)

    fig.text(ref_labvendareal_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', merc_real, True), data, merc_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)
    merc.axhline(0, color='white', xmin = 0, xmax = 1)
    merc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ SERVIÇOS -----------------------------------------------------------

    for val in y_val[:7:-1]:
            serv.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    serv.bar([1,2], [min(serv_ating_real*100, 130),0], width, color = ['#fdee73'], edgecolor = ['#fdee73'], linewidth = 2.6, align = 'edge')

    props = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor='white')

    serv.set_title('Serviços*', fontsize=12, fontweight='bold', loc = 'left', bbox=props, pad = 30)

    serv.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
    serv.axhline(serv_ating_ritmo * 100, color='#ff5b00', xmin = 0.05, xmax = 0.25, linewidth = 3)
    serv.tick_params(axis='y', which='both', left=False)

    current_prize = min(max((round(serv_ating_real*100, 4) - 100)//5 + 1,0), 7)

    for i, val in enumerate(y_val[9:]):
        if (i + 1) == current_prize and (fam_serv == 1):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor='#ffc000')
            color2 = 'black'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#c65102'
        if i % 2 == 1:
            color2 = 'lightgray'
        fig.text(ref_lab100_x + ref_delta_x, ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_serv * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

    if (serv_ating_real*100 >= 90) and (serv_ating_real*100 <100) and (fam_serv == 1):
        weight = 'bold'
        props2 = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor='#ffc000')
        color2 = 'black'
    else:
        weight = 'normal'
        props2 = None
        color2 = '#c65102'
    fig.text(ref_lab100_x + ref_delta_x, ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_serv * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)
    fig.text(ref_labmeta_x + ref_delta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    fig.text(ref_labprem_x + ref_delta_x, ref_labprem_y, 'Prêmio', color='#c65102', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    for tick in serv.yaxis.get_major_ticks()[:8]:
        tick.label.set_color('white')

    for tick in serv.yaxis.get_major_ticks()[10:16:2]:
        tick.label.set_color('lightgray')

    serv.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    if (serv_ating_ritmo >= 0.86) and (serv_ating_ritmo <= 0.9):
        fig.text(ref_labmetaate_x + 1* ref_delta_x, 0.12 + serv_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', serv_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
    elif serv_ating_ritmo < 0.86:
        fig.text(ref_labmetaate_x + 1* ref_delta_x, 0.12 + serv_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', serv_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)


    fig.text(ref_labvendareal_x + ref_delta_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', serv_real, True), data, serv_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)

    serv.axhline(0, color='white', xmin = 0, xmax = 1)
    serv.axhline(0.01, color='white', xmin = 0, xmax = 1)

    if fam_serv == 1:
        fig.text(0.095, 0.02, '*Todas as Famílias de Serviços estão acima de 70%', color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')
    elif fam_serv == 0:
        fig.text(0.095, 0.02, '*Alguma das Famílias de Serviços está abaixo de 70%', color='darkred', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    # ------------------------------------------------ CDC -----------------------------------------------------------

    for val in y_val[:7:-1]:
            cdc.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    cdc.bar([1,2], [min(cdc_ating_real*100, 130),0], width, color = ['#acc2d9'], edgecolor = ['#acc2d9'], linewidth = 2.6, align = 'edge')

    if str(fil_perfil)[2] == '1':
        cdc.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
        cdc.axhline(cdc_ating_ritmo * 100, color='#0652ff', xmin = 0.05, xmax = 0.25, linewidth = 3)
        cdc.tick_params(axis='y', which='both', left=False)

        props = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='white')
        ajuste = 0
        color = 'black'

        current_prize = min(max((round(cdc_ating_real*100, 4) - 100)//5 + 1,0), 7)

        for i, val in enumerate(y_val[9:]):
            if (i + 1) == current_prize:
                weight = 'bold'
                props2 = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='#002060')
                color2 = 'white'
            else:
                weight = 'normal'
                props2 = None
                color2 = '#00035b'
            if i % 2 == 1:
                color2 = 'lightgray'
            fig.text(ref_lab100_x + (2 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_cdc * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        if (cdc_ating_real*100 >= 90) and (cdc_ating_real*100 <100):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='#002060')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#00035b'
        fig.text(ref_lab100_x + (2 *ref_delta_x), ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_cdc * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (2 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#00035b', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

        for tick in cdc.yaxis.get_major_ticks()[:8]:
            tick.label.set_color('white')

        for tick in cdc.yaxis.get_major_ticks()[10:16:2]:
            tick.label.set_color('lightgray')

        cdc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        if (cdc_ating_ritmo >= 0.86) and (cdc_ating_ritmo <= 0.9):
            fig.text(ref_labmetaate_x + 2* ref_delta_x, 0.12 + cdc_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', cdc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
        elif cdc_ating_ritmo < 0.86:
            fig.text(ref_labmetaate_x + 2* ref_delta_x, 0.12 + cdc_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', cdc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)

        fig.text(ref_labvendareal_x + 2*ref_delta_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', cdc_real, True), data, cdc_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)

    else:
        ajuste = 0.02
        color = 'lightgray'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in cdc.yaxis.get_major_ticks():
            tick.label.set_color('lightgray')

    cdc.set_title('  CDC  ', fontsize=12, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)

    fig.text(ref_labmeta_x + (2 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    cdc.axhline(0, color='white', xmin = 0, xmax = 1)
    cdc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ MÓVEIS -----------------------------------------------------------
    for val in y_val[:7:-1]:
            moveis.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    moveis.bar([1,2], [min(moveis_ating_real*100, 130),0], width, color = ['#bcecac'], edgecolor = ['#bcecac'], linewidth = 2.6, align = 'edge')

    if str(fil_perfil)[3] == '1':
        moveis.axhline(100, color='black', xmin = 0.045, xmax = 0.245)
        moveis.axhline(moveis_ating_ritmo * 100, color='#3f9b0b', xmin = 0.05, xmax = 0.25, linewidth = 3)
        moveis.tick_params(axis='y', which='both', left=False)

        props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='white')
        ajuste = 0
        color = 'black'

        current_prize = min(max((round(moveis_ating_real*100, 4) - 100)//5 + 1,0), 7)

        for i, val in enumerate(y_val[9:]):
            if (i + 1) == current_prize:
                weight = 'bold'
                props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
                color2 = 'white'
            else:
                weight = 'normal'
                props2 = None
                color2 = '#06470c'
            if i % 2 == 1:
                color2 = 'lightgray'
            fig.text(ref_lab100_x + (3 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_moveis * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        if (moveis_ating_real*100 >= 90) and (moveis_ating_real*100 <100):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#06470c'
        fig.text(ref_lab100_x + (3 *ref_delta_x), ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_moveis * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (3 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

        for tick in moveis.yaxis.get_major_ticks()[:8]:
            tick.label.set_color('white')

        for tick in moveis.yaxis.get_major_ticks()[10:16:2]:
            tick.label.set_color('lightgray')

        moveis.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        if (moveis_ating_ritmo >= 0.86) and (moveis_ating_ritmo <= 0.9):
            fig.text(ref_labmetaate_x + 3* ref_delta_x, 0.12 + moveis_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', moveis_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
        elif moveis_ating_ritmo < 0.86:
            fig.text(ref_labmetaate_x + 3* ref_delta_x, 0.12 + moveis_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', moveis_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)

        fig.text(ref_labvendareal_x + 3*ref_delta_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', moveis_real, True), data, moveis_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)

    else:
        ajuste = 0.02
        color = 'lightgray'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in moveis.yaxis.get_major_ticks():
            tick.label.set_color('lightgray')

    moveis.set_title(' Móveis ', fontsize=12, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)

    fig.text(ref_labmeta_x + (3 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    moveis.axhline(0, color='white', xmin = 0, xmax = 1)
    moveis.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ ELETROPORTÁTEIS -----------------------------------------------------------
    for val in y_val[:7:-1]:
            port.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    port.bar([1,2], [min(port_ating_real*100, 130),0], width, color = ['#bcecac'], edgecolor = ['#bcecac'], linewidth = 2.6, align = 'edge')

    if str(fil_perfil)[4] == '1':
        port.axhline(100, color='black', xmin = 0.045, xmax = 0.245)
        port.axhline(port_ating_ritmo * 100, color='#3f9b0b', xmin = 0.05, xmax = 0.25, linewidth = 3)
        port.tick_params(axis='y', which='both', left=False)

        props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='white')
        ajuste = 0
        color = 'black'

        current_prize = min(max((round(port_ating_real*100, 4) - 100)//5 + 1,0), 7)

        for i, val in enumerate(y_val[9:]):
            if (i+1) == current_prize:
                weight = 'bold'
                props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
                color2 = 'white'
            else:
                weight = 'normal'
                props2 = None
                color2 = '#06470c'
            if i % 2 == 1:
                color2 = 'lightgray'

            fig.text(ref_lab100_x + (4 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_port * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        if (port_ating_real*100 >= 90) and (port_ating_real*100 <100):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#06470c'
        fig.text(ref_lab100_x + (4 *ref_delta_x), ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_port * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (4 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

        for tick in port.yaxis.get_major_ticks()[:8]:
            tick.label.set_color('white')

        for tick in port.yaxis.get_major_ticks()[10:16:2]:
            tick.label.set_color('lightgray')

        port.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        if (port_ating_ritmo >= 0.86) and (port_ating_ritmo <= 0.9):
            fig.text(ref_labmetaate_x + 4* ref_delta_x, 0.12 + port_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', port_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
        elif port_ating_ritmo < 0.86:
            fig.text(ref_labmetaate_x + 4* ref_delta_x, 0.12 + port_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', port_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)

        fig.text(ref_labvendareal_x + 4 * ref_delta_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', port_real, True), data, port_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)

    else:
        ajuste = 0.02
        color = 'lightgray'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in port.yaxis.get_major_ticks():
            tick.label.set_color('lightgray')

    port.set_title('Eletroportáteis', fontsize=12, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)

    fig.text(ref_labmeta_x + (4 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    port.axhline(0, color='white', xmin = 0, xmax = 1)
    port.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ EMISSÃO DE CARTÕES -----------------------------------------------------------
    for val in y_val[:7:-1]:
            cartao.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    cartao.bar([1,2], [min(cartao_ating_real*100, 130),0], width, color = ['#acc2d9'], edgecolor = ['#acc2d9'], linewidth = 2.6, align = 'edge')

    if str(fil_perfil)[5] == '1':
        cartao.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
        cartao.axhline(cartao_ating_ritmo * 100, color='#0652ff', xmin = 0.05, xmax = 0.25, linewidth = 3)
        cartao.tick_params(axis='y', which='both', left=False)

        props = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='white')
        ajuste = 0
        color = 'black'

        current_prize = min(max((round(cartao_ating_real*100, 4) - 100)//5 + 1,0), 7)

        for i, val in enumerate(y_val[9:]):
            if (i + 1) == current_prize:
                weight = 'bold'
                props2 = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='#002060')
                color2 = 'white'
            else:
                weight = 'normal'
                props2 = None
                color2 = '#00035b'
            if i % 2 == 1:
                color2 = 'lightgray'

            fig.text(ref_lab100_x + (5 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_cartao * (prem_100 + prem_step * i))), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        if (cartao_ating_real*100 >= 90) and (cartao_ating_real*100 <100):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='#002060')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#00035b'
        fig.text(ref_lab100_x + (5 *ref_delta_x), ref_lab100_y - (2* ref_delta_y), 'R$ ' + '{:.0f}'.format(float(target * target_cartao * prem_90)), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (5 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#00035b', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

        for tick in cartao.yaxis.get_major_ticks()[:8]:
            tick.label.set_color('white')

        for tick in cartao.yaxis.get_major_ticks()[10:16:2]:
            tick.label.set_color('lightgray')

        cartao.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        if (cartao_ating_ritmo >= 0.86) and (cartao_ating_ritmo <= 0.9):
            fig.text(ref_labmetaate_x + 5 * ref_delta_x, 0.12 + cartao_ating_ritmo*0.49, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', cartao_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)
        elif cartao_ating_ritmo < 0.86:
            fig.text(ref_labmetaate_x + 5 * ref_delta_x, 0.12 + cartao_ating_ritmo*0.53, 'Meta até {}\n$\\bf{}$'.format(data, locale.format('%.0f', cartao_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 9)

        fig.text(ref_labvendareal_x + 5 * ref_delta_x, 0.06, 'Realizado até {}: $\\bf{}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', cartao_real, True), data, cartao_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 9)

    else:
        ajuste = 0.02
        color = 'lightgray'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in cartao.yaxis.get_major_ticks():
            tick.label.set_color('lightgray')

    cartao.set_title(' Cartões ', fontsize=12, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)

    fig.text(ref_labmeta_x + (5 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    cartao.axhline(0, color='white', xmin = 0, xmax = 1)
    cartao.axhline(0.01, color='white', xmin = 0, xmax = 1)

    #---------------------------------------------------------------- NPS -----------------------------------------------------------

    if nps_ating_real >= 1:
        prem_nps = map_fil_porte_prem_nps[fil_porte]
    else:
        prem_nps = 0

    props3 = dict(boxstyle='round', facecolor='dimgray', alpha=0.9)

    fig.text(ref_labvendareal_x + 4.3 * ref_delta_x, 0.01, 'Atingimento NPS: $\\bf{}\%$'.format(locale.format('%.0f', nps_ating_real * 100 )), color='white', horizontalalignment = 'left', fontsize = 9, bbox = props3)
    fig.text(ref_labvendareal_x + 5.1 * ref_delta_x, 0.01, 'Prêmio Adicional NPS: $\\bfR\$ {} $'.format(locale.format('%.0f', prem_nps)), color='white', horizontalalignment = 'left', fontsize = 9, bbox = props3)

    # --------------------------------------------------------------- AJUSTES FINAIS -------------------------------------------------

    # Watermark com Matrícula do funcionário
    fig.text(0.5, 0.2, str(cd_fun), fontsize=80, color='gray', ha='center', va='center', alpha=0.12)

    # Texto Atingimento da Meta Mensal
    fig.text(0.095, ref_labmeta_y, 'Ating.\nMeta\nMensal', color='black', fontweight='bold', horizontalalignment = 'left', fontsize = 11)

    # Nota sobre data de atualização dos dados
    fig.text(0.095, 0.975, 'Dados atualizados até {}'.format(data), color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    # Texto com Porte da Loja
    fig.text(0.825, 0.975, 'Porte da loja: $\\bf{}$'.format(fil_porte), color = 'black', horizontalalignment = 'left', fontsize = 10)

    fig.set_facecolor('white')
    serv.axhline(0, color='white', xmin = 0, xmax = 1)
    serv.axhline(0.01, color='white', xmin = 0, xmax = 1)

    if fam_serv == 1:
        fig.text(0.095, 0.02, '*Todas as Famílias de Serviços estão acima de 70%', color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')
    elif fam_serv == 0:
        fig.text(0.095, 0.02, '*Alguma das Famílias de Serviços está abaixo de 70%', color='darkred', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    fig.savefig('./gerente/grafico_mensal/{}.png'.format(str(cd_fun)), bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
        df_loja = pd.read_excel('./inputs/Apuração RV Gerentes - Mensal_{}.xlsx'.format(DT_TODAY_FILE), sheet_name='Apuração Preliminar', skiprows=1)
        df_piloto = pd.read_excel('./inputs/Mod. de Premiação - Perfis e Portes de Loja v07_MAR-2019.xlsx', sheet_name='BD FILIAIS')
        df_loja.drop(columns = [col for col in df_loja if 'Unnamed:' in col], inplace = True)
        df_rot = pd.read_csv('./inputs/roteirizacao.csv', encoding='latin-1')

        # Filtra somente as colunas relevantes e as renomeia
        df_loja = df_loja[list(rename_dict.keys())].rename(columns = rename_dict)
        df_loja = pd.merge(df_loja,df_rot[['CD_FIL','CD_FUN_GER','NOME_GERENTE_LOJA']],on='CD_FIL',how='left')
        df_piloto = df_piloto.rename(columns = {'Filial':'CD_FIL'})
        df_loja = pd.merge(df_piloto,df_loja, on = 'CD_FIL', how = 'left')
        df_loja = df_loja[~df_loja['CD_FUN_GER'].isnull()].reset_index().drop(columns = 'index')
        df_loja['NOME_GERENTE_LOJA'] = df_loja['NOME_GERENTE_LOJA'].apply(lambda x: x.split()[0].capitalize())
        df_loja['CD_FUN_GER'] = df_loja['CD_FUN_GER'].astype(int).astype(str)
        df_loja['ICM_CDC'] = df_loja['ICM_CDC'].fillna(0)
        df_loja['DT_NPS'] = df_loja['DT_NPS'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])
        df_loja['DT_CART'] = df_loja['DT_CART'].apply(lambda x: x.strftime('%d/') + month_dict[int(x.strftime('%d/%m')[-2:])])

        porte_loja = re.compile(r'PORTE ')

        df_loja['PORTE_NUMBER'] = df_loja['PORTE COM RETIRA'].apply(lambda x: re.sub(porte_loja,'',x))
        df_loja.PORT_META_ACU = df_loja.PORT_META_ACU.fillna(0)
        df_loja['CD_FUN_GER'] = df_loja.CD_FUN_GER.astype(int) + 2100000000

        mp_handler(df_loja)