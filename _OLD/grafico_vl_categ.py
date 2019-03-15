import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import locale

perc_ating = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 105, 110, 115, 120, 125, 130]


def get_ylabels(meta_total):
    aux = perc_ating.copy()
    for i, perc in enumerate(aux):
        aux[i] = 'R$ ' + locale.format('%.0f', int(perc * meta_total / 100), True)

    return aux


def gerar_imagem_vl_categ(cd_fun, cd_fil, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu,
                     cdc_real, cdc_meta_tot, cdc_meta_acu, dia, mes):
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
    if cdc_meta_tot != 0:
        cdc_ating_real = cdc_real / cdc_meta_tot
        cdc_ating_ritmo = cdc_meta_acu / cdc_meta_tot
    else:
        cdc_ating_real = 0
        cdc_ating_ritmo = 0
    cdc_ating_acu = cdc_real / cdc_meta_acu

    data = '{:02d}/{:02d}'.format(dia,mes)

        # PARÂMETROS DE PREMIAÇÃO (Versão com e sem meta de CDC)
    if cdc_meta_tot != 0:
        merc_prem_90 = 240
        merc_prem_100 = 480
        merc_prem_step = 48
        serv_prem_90 = 210
        serv_prem_100 = 420
        serv_prem_step = 42
        cdc_prem_90 = 210
        cdc_prem_100 = 420
        cdc_prem_step = 42
    else:
        merc_prem_90 = 240
        merc_prem_100 = 480
        merc_prem_step = 48
        serv_prem_90 = 210
        serv_prem_100 = 420
        serv_prem_step = 42
        cdc_prem_90 = 0
        cdc_prem_100 = 0
        cdc_prem_step = 0

    # COORDENADAS DO GRÁFICO P/ LABELS AUX
    # Labels Prêmio (e.g. R$ 480, R$ 420)
    ref_lab100_y = 0.67 # 0.658
    ref_lab100_x = 0.308 # 0.156
    ref_delta_y = 0.028 # 0.0315

    # Label "Meta de Venda" p/ eixo Y
    ref_labmeta_y = 0.87 # 0.878
    ref_labmeta_x = 0.205 # 0.052

    # Label "Prêmio"
    ref_labprem_y = 0.87 # 0.875
    ref_labprem_x = 0.33 # 0.173

    # Delta entre um gráfico e outro (eixo X)
    ref_delta_x = 0.223 # 0.327

    #Label "Meta até"
    ref_labmetaate_x = 0.294

    #Label "Venda Realizada"
    ref_labvendareal_x = 0.2

    # Criação da Figura
    fig = plt.figure(figsize=(12.8, 7.2), dpi = 80)

    # Configuração do Grid
    gs0 = gridspec.GridSpec(1, 35, figure=fig)

    # Subplot com o Eixo dos atingimentos % (até 130%)
    ax1 = plt.Subplot(fig, gs0[:,0:5], frame_on = False)
    fig.add_subplot(ax1)

    # Subplot Mercantil
    merc = plt.Subplot(fig, gs0[:,5:15], frame_on = False)
    fig.add_subplot(merc)

    # Subplot Serviços
    serv = plt.Subplot(fig, gs0[:,15:25], frame_on = False)
    fig.add_subplot(serv)

    # Subplot CDC
    cdc = plt.Subplot(fig, gs0[:,25:35], frame_on = False)
    fig.add_subplot(cdc)

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
    merc.tick_params(axis='y', which='both', left=False)

    serv.set_yticks(y_val)
    serv.set_yticklabels(get_ylabels(serv_meta_tot), fontsize=11)
    serv.set_xticks([])
    serv.tick_params(axis='y', which='both', left=False)

    cdc.set_yticks(y_val)
    cdc.set_yticklabels(get_ylabels(cdc_meta_tot), fontsize=11)
    cdc.set_xticks([])
    cdc.tick_params(axis='y', which='both', left=False)

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

    # init = merc_prem_min + get_acelerador(serv_ating_acu, cdc_ating_acu, cdc_meta_tot)

    current_prize = min(max((merc_ating_real*100 - 100)//5 + 1,0), 7)

    for i, val in enumerate(y_val[9:]):
        if (i + 1) == current_prize:
            weight = 'bold'
            props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
            color = 'white'
        else:
            weight = 'normal'
            props = None
            color = '#06470c'
        if i % 2 == 1:
            color = 'lightgray'
        fig.text(ref_lab100_x, ref_lab100_y + (i* ref_delta_y), 'R$ ' + str(merc_prem_100 + merc_prem_step * i), color=color, fontsize=11, fontweight = weight, bbox=props)

    if (merc_ating_real*100 >= 90) and (merc_ating_real*100 <100):
        weight = 'bold'
        props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
        color = 'white'
    else:
        weight = 'normal'
        props = None
        color = '#06470c'
    fig.text(ref_lab100_x, ref_lab100_y - (2* ref_delta_y), 'R$ ' + str(merc_prem_90), color=color, fontsize=11, fontweight = weight, bbox=props)

    fig.text(ref_labmeta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    for tick in merc.yaxis.get_major_ticks()[:8]:
        tick.label.set_color('white')

    for tick in merc.yaxis.get_major_ticks()[10:16:2]:
        tick.label.set_color('lightgray')

    merc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    if (merc_ating_ritmo >= 0.86) and (merc_ating_ritmo <= 0.9):
        fig.text(ref_labmetaate_x, 0.12 + merc_ating_ritmo*0.485, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', merc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)
    elif merc_ating_ritmo < 0.86:
        fig.text(ref_labmetaate_x, 0.12 + merc_ating_ritmo*0.53, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', merc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

    fig.text(ref_labvendareal_x, 0.06, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', merc_real, True), data, merc_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 10)
    merc.axhline(0, color='white', xmin = 0, xmax = 1)
    merc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ SERVIÇOS -----------------------------------------------------------

    for val in y_val[:7:-1]:
            serv.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    serv.bar([1,2], [min(serv_ating_real*100, 130),0], width, color = ['#fdee73'], edgecolor = ['#fdee73'], linewidth = 2.6, align = 'edge')

    props = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor = 'white')

    serv.set_title('Serviços', fontsize=12, fontweight='bold', loc = 'left', bbox=props, pad = 30)

    serv.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
    serv.axhline(serv_ating_ritmo * 100, color='#ff5b00', xmin = 0.05, xmax = 0.25, linewidth = 3)

    current_prize = min(max((serv_ating_real*100 - 100)//5 + 1,0), 7)

    for i, val in enumerate(y_val[9:]):
        if (i + 1) == current_prize:
            weight = 'bold'
            props = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor='#ffc000')
            color = 'black'
        else:
            weight = 'normal'
            props = None
            color = '#bf9005'
        if i % 2 == 1:
            color = 'lightgray'
        fig.text(ref_lab100_x + ref_delta_x, ref_lab100_y + (i* ref_delta_y), 'R$ ' + str(serv_prem_100 + serv_prem_step*i), color=color, fontsize=11, fontweight = weight, bbox=props)

    if (serv_ating_real*100 >= 90) and (serv_ating_real*100 <100):
        weight = 'bold'
        props = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8, edgecolor='#ffc000')
        color = 'black'
    else:
        weight = 'normal'
        props = None
        color = '#bf9005'
    fig.text(ref_lab100_x + ref_delta_x, ref_lab100_y - (2* ref_delta_y), 'R$ ' + str(serv_prem_90), color=color, fontsize=11, fontweight = weight, bbox=props)

    fig.text(ref_labmeta_x + ref_delta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    fig.text(ref_labprem_x + ref_delta_x, ref_labprem_y, 'Prêmio', color='#bf9005', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    for tick in serv.yaxis.get_major_ticks()[:8]:
        tick.label.set_color('white')

    for tick in serv.yaxis.get_major_ticks()[10:16:2]:
        tick.label.set_color('lightgray')

    serv.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    if (serv_ating_ritmo >= 0.86) and (serv_ating_ritmo <= 0.9):
        fig.text(ref_labmetaate_x + ref_delta_x, 0.12 + serv_ating_ritmo*0.485, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', serv_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)
    elif serv_ating_ritmo < 0.86:
        fig.text(ref_labmetaate_x + ref_delta_x, 0.12 + serv_ating_ritmo*0.53, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', serv_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

    fig.text(ref_labvendareal_x + ref_delta_x, 0.065, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', serv_real, True), data, serv_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 10)
    serv.axhline(0, color='white', xmin = 0, xmax = 1)
    serv.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # ------------------------------------------------ CDC -----------------------------------------------------------

    for val in y_val[:7:-1]:
            cdc.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    cdc.bar([1,2], [min(cdc_ating_real*100, 130),0], width, color = ['#acc2d9'], edgecolor = ['#acc2d9'], linewidth = 2.6, align = 'edge')


    if cdc_meta_tot != 0:
        cdc.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
        cdc.axhline(cdc_ating_ritmo * 100, color='#0652ff', xmin = 0.05, xmax = 0.25, linewidth = 3)

        props = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor = 'white')
        ajuste = 0
        color = 'black'

        current_prize = min(max((cdc_ating_real*100 - 100)//5 + 1,0), 7)

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
            fig.text(ref_lab100_x + (2 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), 'R$ ' + str(cdc_prem_100 + cdc_prem_step * i), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        if (cdc_ating_real*100 >= 90) and (cdc_ating_real*100 <100):
            weight = 'bold'
            props2 = dict(boxstyle='round', facecolor='#002060', alpha=0.8, edgecolor='#002060')
            color2 = 'white'
        else:
            weight = 'normal'
            props2 = None
            color2 = '#00035b'
        fig.text(ref_lab100_x + (2 *ref_delta_x), ref_lab100_y - (2* ref_delta_y), 'R$ ' + str(cdc_prem_90), color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (2 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#00035b', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

        for tick in cdc.yaxis.get_major_ticks()[:8]:
            tick.label.set_color('white')

        for tick in cdc.yaxis.get_major_ticks()[10:16:2]:
            tick.label.set_color('lightgray')

        cdc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        if (cdc_ating_ritmo >= 0.86) and (cdc_ating_ritmo <= 0.9):
            fig.text(ref_labmetaate_x + 2*ref_delta_x, 0.12 + cdc_ating_ritmo*0.485, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', cdc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)
        elif cdc_ating_ritmo < 0.86:
            fig.text(ref_labmetaate_x + 2*ref_delta_x, 0.12 + cdc_ating_ritmo*0.53, 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', cdc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

        fig.text(ref_labvendareal_x + 2*ref_delta_x, 0.065, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', cdc_real, True), data, cdc_ating_acu*100), color='black', horizontalalignment = 'left', fontsize = 10)


    else:
        ajuste = 0.02
        color = 'gray'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in cdc.yaxis.get_major_ticks():
            tick.label.set_color('gray')

    cdc.set_title('  CDC  ', fontsize=12, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)
    fig.text(ref_labmeta_x + (2 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    cdc.axhline(0, color='white', xmin = 0, xmax = 1)
    cdc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    # --------------------------------------------------------------- AJUSTES FINAIS -------------------------------------------------

    # Watermark com Matrícula do funcionário
    fig.text(0.70, 0.08, str(cd_fun), fontsize=80, color='gray', ha='right', va='bottom', alpha=0.12)

    # Texto Atingimento da Meta Mensal
    fig.text(0.08, ref_labmeta_y, 'Ating.\nMeta\nMensal', color='black', fontweight='bold', horizontalalignment = 'left', fontsize = 11)

    # Nota sobre data de atualização dos dados
    fig.text(0.08, 0.975, 'Dados atualizados até {}'.format(data), color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    fig.text(0.07, 0.5, 'Prêmio Líder Categoria', color='black', horizontalalignment = 'right', verticalalignment = 'center', rotation = 'vertical', fontsize = 20, fontstyle='normal', fontweight='bold')
    fig.set_facecolor('white')

    return fig