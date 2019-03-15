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


def get_acelerador(serv_ating, cdc_ating, cdc_meta_tot):

    if cdc_meta_tot != 0:
        aux = min(serv_ating, cdc_ating)
    else:
        aux = serv_ating

    if aux >= 0.9:
        return 10
    elif aux >= 0.8:
        return 5
    elif aux >= 0.7:
        return 1
    else:
        return 0


def gerar_imagem_vc(cd_fun, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu, cdc_real, cdc_meta_tot, cdc_meta_acu, dia, mes):

    check_img = plt.imread('./images/check.png')
    cross_img = plt.imread('./images/cross.png')
    flag_white_img = plt.imread('./images/flag_white.png')
    flag_gray_img = plt.imread('./images/flag_gray.png')
    target_img = plt.imread('./images/target.png')
    cashG_img = plt.imread('./images/cash_green.png')
    cashO_img = plt.imread('./images/cash_orange.png')
    cashB_img = plt.imread('./images/cash_blue.png')

    # DEFINIÇÃO DE LOCALE para utilizar formatação com separador de milhar como '.'
    locale.setlocale(locale.LC_ALL, 'German')

    # CRIAÇÃO DE ATINGIMENTOS

    # Mercantil
    merc_ating_real = merc_real / merc_meta_tot
    merc_ating_ritmo = merc_meta_acu / merc_meta_tot
    if merc_meta_acu != 0:
        merc_ating_acu = merc_real / merc_meta_acu
    else:
        merc_ating_acu = 0

    # Serviços
    serv_ating_real = serv_real / serv_meta_tot
    serv_ating_ritmo = serv_meta_acu / serv_meta_tot
    if serv_meta_acu != 0:
        serv_ating_acu = serv_real / serv_meta_acu
    else:
        serv_ating_acu = 0

    # CDC
    if cdc_meta_tot != 0:
        cdc_ating_real = cdc_real / cdc_meta_tot
        cdc_ating_ritmo = cdc_meta_acu / cdc_meta_tot
        cdc_ating_acu = cdc_real / cdc_meta_acu
    else:
        cdc_ating_real = 0
        cdc_ating_ritmo = 0
        cdc_ating_acu = 0

    # Ajustando a data
    data = '{:02d}/{:02d}'.format(dia,mes)


    # PARÂMETROS DE PREMIAÇÃO (Versão com e sem meta de CDC)
    if cdc_meta_tot != 0:
        merc_prem_min = 5
        merc_prem_step = 1.5
        merc_add = 2
        serv_prem_min = 10
        serv_prem_step = 1.5
    else:
        merc_prem_min = 10
        merc_prem_step = 2.5
        merc_add = 3
        serv_prem_min = 15
        serv_prem_step = 2


    # COORDENADAS DO GRÁFICO P/ LABELS AUX
    # Labels Prêmio (e.g. 10%, 11.5%)
    ref_lab100_y = 0.6675
    ref_lab100_x = 0.298
    ref_delta_y = 0.0275

    # Label "Meta de Venda" p/ eixo Y
    ref_labmeta_y = 0.86
    ref_labmeta_x = 0.202

    # Label "Premiação"
    ref_labprem_y = 0.86
    ref_labprem_x = 0.318

    # Delta entre um gráfico e outro (eixo X)
    ref_delta_x = 0.225

    # ------------------------------------------------ CRIAÇÃO DA FIGURA -----------------------------------------------------------

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
    ax1.tick_params(
    axis='y',
    which='both',
    left=False)

    ax1.bar([1], [max(y_val)], width, color = ['#ffffff'], edgecolor = ['#ffffff'], linewidth = 0, align = 'edge')

    for tick in ax1.yaxis.get_major_ticks()[:6]:
        tick.label.set_color('white')

    for tick in ax1.yaxis.get_major_ticks()[6:9]:
        tick.label.set_color('lightgray')

    merc.set_yticks(y_val)
    merc.set_yticklabels(get_ylabels(merc_meta_tot), fontsize=11)
    merc.set_xticks([])
    merc.tick_params(
    axis='y',
    which='both',
    left=False)

    serv.set_yticks(y_val)
    serv.set_yticklabels(get_ylabels(serv_meta_tot), fontsize=11)
    serv.set_xticks([])
    serv.tick_params(
    axis='y',
    which='both',
    left=False)

    cdc.set_yticks(y_val)
    cdc.set_yticklabels(get_ylabels(cdc_meta_tot), fontsize=11)
    cdc.set_xticks([])
    cdc.tick_params(
    axis='y',
    which='both',
    left=False)


    # ------------------------------------------------ MERCANTIL -----------------------------------------------------------

    p_cor = ['#ffffff'] # cores de preenchimento das barras em HEX https://xkcd.com/color/rgb/
    p_edcor = ['#929591'] # cores da borda das barras em HEX https://xkcd.com/color/rgb/
    p_lw = 1.2 # espessura das linhas
    p_ls = '--'

    for val in y_val[:8:-1]:
            merc.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    merc.bar([1,2], [min(merc_ating_real*100, 130),0], width, color = ['#bcecac'], edgecolor = ['#bcecac'], linewidth = 2.6, align = 'edge')

    props = dict(boxstyle='round', facecolor='#006600', alpha=0.8)

    merc.set_title('Mercantil', fontsize=16, fontweight='bold', color='white', loc = 'left', bbox=props, pad = 30)

    merc.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
    merc.axhline(merc_ating_ritmo * 100, color='#3f9b0b', xmin = 0.05, xmax = 0.25, linewidth = 3)

    init = merc_prem_min + get_acelerador(serv_ating_real, cdc_ating_real, cdc_meta_tot)

    current_prize = min(max((merc_ating_real*100 - 100)//5 + 1,0), 7)

    for i, val in enumerate(y_val[9:]):
        if (i + 1) == current_prize:
            weight = 'bold'
            props = dict(boxstyle='round', facecolor='#006600', alpha=0.8, edgecolor='#006600')
            color = 'white'
        else:
            weight = 'normal'
            props = None

            if i % 2 == 1:
                color = 'lightgray'
            else:
                color = '#06470c'


        if (i == (len(y_val[9:]) - 1)) and (get_acelerador(serv_ating_acu, cdc_ating_acu, cdc_meta_tot) == 10):
            adicional_130 = True
        else:
            adicional_130 = False

        fig.text(ref_lab100_x, ref_lab100_y + (i* ref_delta_y), locale.format('%.1f', init + merc_prem_step*i + merc_add*adicional_130) + '%', color=color, fontsize=11, fontweight = weight, bbox=props)


    fig.text(ref_labmeta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)


    if get_acelerador(serv_ating_real, cdc_ating_real, cdc_meta_tot) == 0:
        fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio sem\nAcelerador', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    elif get_acelerador(serv_ating_real, cdc_ating_real, cdc_meta_tot) == 1:
        fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio com\nAcelerador 70%', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    elif get_acelerador(serv_ating_real, cdc_ating_real, cdc_meta_tot) == 5:
        fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio com\nAcelerador 80%', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    elif get_acelerador(serv_ating_real, cdc_ating_real, cdc_meta_tot) == 10:
        fig.text(ref_labprem_x, ref_labprem_y, 'Prêmio com\nAcelerador 90%', color='#06470c', fontweight='bold', horizontalalignment = 'center', fontsize = 11)


    for tick in merc.yaxis.get_major_ticks()[:6]:
        tick.label.set_color('white')

    for tick in merc.yaxis.get_major_ticks()[6:9]:
        tick.label.set_color('lightgray')

    merc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    fig.text(0.294, min(0.105 + merc_ating_ritmo*0.55, 0.615), 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', merc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

    if merc_ating_real >= merc_ating_ritmo:
        fig.figimage(check_img, xo=193, yo=15)
        color='#06470c'
    else:
        fig.figimage(cross_img, xo=193, yo=15)
        color='#840000'

    fig.text(0.2, 0.065, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', merc_real, True), data, merc_ating_acu*100), color=color, horizontalalignment = 'left', fontsize = 10)


    # ------------------------------------------------ SERVIÇOS -----------------------------------------------------------

    for val in y_val[:5:-1]:
            serv.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    if serv_ating_real < serv_ating_ritmo:
        color = ['#ff474c']
    else:
        color = ['#5ca904']


    serv.bar([1,2], [min(serv_ating_real*100, 130),0], width, color = ['#fdee73'], edgecolor = ['#fdee73'], linewidth = 2.6, align = 'edge')

    props = dict(boxstyle='round', facecolor='#ffc000', alpha=0.8)

    serv.set_title('Serviços', fontsize=16, fontweight='bold', loc = 'left', bbox=props, pad = 30)

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

            if i % 2 == 1:
                color = 'lightgray'
            else:
                color = '#c65102'

        if i == (len(y_val[9:]) - 1):
            adicional_130 = True
        else:
            adicional_130 = False


        fig.text(ref_lab100_x + ref_delta_x, ref_lab100_y + (i* ref_delta_y), locale.format('%.1f', float(serv_prem_min + serv_prem_step*i + adicional_130)) + '%', color=color, fontsize=11, fontweight = weight, bbox=props)


    fig.text(ref_labmeta_x + ref_delta_x, ref_labmeta_y, 'Meta\nMensal', color='black', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
    fig.text(ref_labprem_x + ref_delta_x, ref_labprem_y, 'Prêmio', color='#c65102', fontweight='bold', horizontalalignment = 'center', fontsize = 11)

    for tick in serv.yaxis.get_major_ticks()[:6]:
        tick.label.set_color('white')

    for tick in serv.yaxis.get_major_ticks()[6:9]:
        tick.label.set_color('lightgray')

    serv.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

    fig.text(0.294 + ref_delta_x, min(0.105 + serv_ating_ritmo*0.55, 0.615), 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', serv_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

    if serv_ating_real >= serv_ating_ritmo:
        fig.figimage(check_img, xo=193 + 229, yo=15)
        color='#06470c'
    else:
        fig.figimage(cross_img, xo=193 + 229, yo=15)
        color='#840000'

    fig.text(0.2 + ref_delta_x, 0.065, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', serv_real, True), data, serv_ating_acu*100), color=color, horizontalalignment = 'left', fontsize = 10)


    # ------------------------------------------------ CDC -----------------------------------------------------------

    for val in y_val[:5:-1]:
            cdc.bar([1,2], [val, 0], width, color = p_cor, edgecolor = p_edcor, linewidth = p_lw, linestyle = p_ls, align = 'edge')

    cdc.bar([1,2], [min(cdc_ating_real*100, 130),0], width, color = ['#acc2d9'], edgecolor = ['#acc2d9'], linewidth = 2.6, align = 'edge')


    if cdc_meta_tot != 0:
        cdc.axhline(100, color='black', xmin = 0.05, xmax = 0.25)
        cdc.axhline(cdc_ating_ritmo * 100, color='#0652ff', xmin = 0.05, xmax = 0.25, linewidth = 3)

        props = dict(boxstyle='round', facecolor='#002060', alpha=0.8)
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

                if i % 2 == 1:
                    color2 = 'lightgray'
                else:
                    color2 = '#00035b'


            if i == (len(y_val[9:]) - 1):
                adicional_130 = True
            else:
                adicional_130 = False

            fig.text(ref_lab100_x + (2 *ref_delta_x), ref_lab100_y + (i* ref_delta_y), locale.format('%.1f', 10 + 1.5*i + adicional_130) + '%', color=color2, fontsize=11, fontweight = weight, bbox=props2)

        fig.text(ref_labprem_x + (2 * ref_delta_x), ref_labprem_y, 'Prêmio', color='#00035b', fontweight='bold', horizontalalignment = 'center', fontsize = 11)
        for tick in cdc.yaxis.get_major_ticks()[:6]:
            tick.label.set_color('white')

        for tick in cdc.yaxis.get_major_ticks()[6:9]:
            tick.label.set_color('lightgray')

        cdc.yaxis.get_major_ticks()[9].label.set_fontweight('bold')

        fig.text(0.294 + 2*ref_delta_x, min(0.105 + cdc_ating_ritmo*0.55, 0.615), 'Meta até {}\n$\\bfR\$ {}$'.format(data, locale.format('%.0f', cdc_meta_acu, True)), color='black', horizontalalignment = 'left', fontsize = 10)

        if cdc_ating_real >= cdc_ating_ritmo:
            fig.figimage(check_img, xo=193 + 458, yo=15)
            color2='#06470c'
        else:
            fig.figimage(cross_img, xo=193 + 458, yo=15)
            color2='#840000'

        fig.text(0.2 + 2*ref_delta_x, 0.065, 'Realizado até {}: $\\bfR\$ {}$ \n% da Meta até {}: $\\bf{:.0f}\%$'.format(data, locale.format('%.0f', cdc_real, True), data,cdc_ating_acu*100), color=color2, horizontalalignment = 'left', fontsize = 10)

    else:
        ajuste = 0.02
        color = 'white'
        props = dict(boxstyle='round', facecolor='#000000', alpha=0.2)

        for tick in cdc.yaxis.get_major_ticks():
            tick.label.set_color('white')


    cdc.set_title('  CDC  ', fontsize=18, fontweight='bold', color = 'white', loc = 'left', bbox=props, pad = 30)

    fig.text(ref_labmeta_x + (2 * ref_delta_x) + ajuste, ref_labmeta_y, 'Meta\nMensal', color=color, fontweight='bold', horizontalalignment = 'center', fontsize = 11)


    # --------------------------------------------------------------- AJUSTES FINAIS -------------------------------------------------

    # Watermark com Matrícula do funcionário
    fig.text(0.5, 0.08, str(cd_fun), fontsize=80, color='gray', ha='center', va='center', alpha=0.12)

    # Nota sobre data de atualização dos dados
    fig.text(0.08, 0.975, 'Dados atualizados até {}'.format(data), color='black', horizontalalignment = 'left', fontsize = 10, fontstyle='italic')

    merc.axhline(0, color='white', xmin = 0, xmax = 1)
    merc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    serv.axhline(0, color='white', xmin = 0, xmax = 1)
    serv.axhline(0.01, color='white', xmin = 0, xmax = 1)

    cdc.axhline(0, color='white', xmin = 0, xmax = 1)
    cdc.axhline(0.01, color='white', xmin = 0, xmax = 1)

    for t in [10,12,14]:
        ax1.yaxis.get_major_ticks()[t].label.set_color('lightgray')
        merc.yaxis.get_major_ticks()[t].label.set_color('lightgray')
        serv.yaxis.get_major_ticks()[t].label.set_color('lightgray')
        if cdc_meta_tot != 0:
            cdc.yaxis.get_major_ticks()[t].label.set_color('lightgray')

    fig.text(0.075, ref_labmeta_y + 0.005, 'Ating.\nMeta\nMensal', color='black', fontweight='bold', horizontalalignment = 'left', fontsize = 11)

    x_init = 392 # 460
    x_add = 228

    y_init = 286
    y_add = 32

    for i in range(3):
        if serv_ating_real >= (0.7 + (0.1 * i)):
            fig.figimage(flag_gray_img, xo = x_init, yo = y_init + y_add * i, zorder=2)
        else:
            fig.figimage(flag_white_img, xo = x_init, yo = y_init + y_add * i, zorder=2)

        if cdc_ating_real >= (0.7 + (0.1 * i)) and cdc_meta_tot != 0:
            fig.figimage(flag_gray_img, xo = x_init + x_add, yo = y_init + y_add * i, zorder=2)
        elif cdc_meta_tot != 0:
            fig.figimage(flag_white_img, xo = x_init + x_add, yo = y_init + y_add * i, zorder=2)

    x_add = 229.5

    fig.figimage(target_img, xo = 98, yo = 511, zorder=2)
    fig.figimage(cashG_img, xo = 196, yo = 511, zorder=2)

    fig.figimage(target_img, xo = 98 + x_add, yo = 511, zorder=2)
    fig.figimage(cashO_img, xo = 443, yo = 496, zorder=2)

    if cdc_meta_tot != 0:
        fig.figimage(target_img, xo = 98 + (2* x_add), yo = 511, zorder=2)
        fig.figimage(cashB_img, xo = 443 + x_add, yo = 496, zorder=2)

    fig.set_facecolor('white')

    return fig