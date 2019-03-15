import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import locale

perc_ating = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 105, 110, 115, 120, 125, 130]


def get_ylabels(meta_total):
    aux = perc_ating.copy()
    for i, perc in enumerate(aux):
        aux[i] = locale.format('%.0f', int(perc * meta_total / 100), True)

    return aux

def get_ylabels2(meta_total):
    aux = perc_ating.copy()
    for i, perc in enumerate(aux):
        aux[i] = locale.format('%.0f', int(perc * meta_total / 100), True)

    return aux

def gerar_imagem_vl_loja(cd_fun, cd_fil, fil_perfil, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu,
cdc_real, cdc_meta_tot, cdc_meta_acu, moveis_real, moveis_meta_tot, moveis_meta_acu,
port_real, port_meta_tot, port_meta_acu, cartao_real, cartao_meta_tot, cartao_meta_acu, fam_serv, nps_real, nps_meta_tot, dia, mes):
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
        cartao_ating_acu = cartao_real / cartao_meta_acu
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

    # PARÂMETROS DE PREMIAÇÃO (Versão com e sem meta de CDC)
    prem_90 = 0.5
    prem_100 = 1
    prem_step = 0.1

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

    data = '{:02d}/{:02d}'.format(dia,mes)

    # figsize=(12.8, 7.2), dpi = 80
    fig = plt.figure(figsize=(20, 7.2), dpi = 80)

    # Configuração do Grid
    gs0 = gridspec.GridSpec(1, 77, figure=fig)

    # Subplot com o Eixo dos atingimentos % (até 130%)
    ax1 = plt.Subplot(fig, gs0[:,2:7], frame_on = False)
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

    target = 1200
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
        prem_nps = 120
    else:
        prem_nps = 0

    props3 = dict(boxstyle='round', facecolor='dimgray', alpha=0.9)

    fig.text(ref_labvendareal_x + 4.3 * ref_delta_x, 0.01, 'Atingimento NPS: $\\bf{}\%$'.format(locale.format('%.0f', nps_ating_real * 100 )), color='white', horizontalalignment = 'left', fontsize = 9, bbox = props3)
    fig.text(ref_labvendareal_x + 5.1 * ref_delta_x, 0.01, 'Prêmio Adicional NPS: $\\bfR\$ {} $'.format(locale.format('%.0f', prem_nps)), color='white', horizontalalignment = 'left', fontsize = 9, bbox = props3)

    # --------------------------------------------------------------- AJUSTES FINAIS -------------------------------------------------

    # Watermark com Matrícula do funcionário
    fig.text(0.5, 0.2, str(cd_fun), fontsize=80, color='gray', ha='center', va='center', alpha=0.12)

    # Texto Atingimento da Meta Mensal
    fig.text(0.115, ref_labmeta_y, 'Ating.\nMeta\nMensal', color='black', fontweight='bold', horizontalalignment = 'left', fontsize = 11)

    # Nota sobre data de atualização dos dados
    fig.text(0.115, 0.975, 'Dados atualizados até {}'.format(data), color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    fig.set_facecolor('white')
    serv.axhline(0, color='white', xmin = 0, xmax = 1)
    serv.axhline(0.01, color='white', xmin = 0, xmax = 1)

    if fam_serv == 1:
        fig.text(0.115, 0.02, '*Todas as Famílias de Serviços estão acima de 70%', color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')
    elif fam_serv == 0:
        fig.text(0.115, 0.02, '*Alguma das Famílias de Serviços está abaixo de 70%', color='darkred', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    fig.text(0.11, 0.5, 'Prêmio Líder Loja', color = 'black', fontsize = 20, horizontalalignment = 'right', verticalalignment = 'center', rotation = 'vertical', fontweight = 'bold')

    return fig