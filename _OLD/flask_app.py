# coding=utf-8
from flask import Flask, render_template, Response, request
import logging
from grafico_vendedor import gerar_imagem_vc
from grafico_gerente_mensal import gerar_imagem_glm
from grafico_vl_categ import gerar_imagem_vl_categ
from grafico_vl_loja import gerar_imagem_vl_loja

import io

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/vendedor/grafico', methods=['GET','POST'])
def plot_vendedor():
    cd_fun = int(request.args.get('cd_fun'))

    merc_real = int(request.args.get('merc_real'))
    merc_meta_tot = int(request.args.get('merc_meta_tot'))
    merc_meta_acu = int(request.args.get('merc_meta_acu'))

    serv_real = int(request.args.get('serv_real'))
    serv_meta_tot = int(request.args.get('serv_meta_tot'))
    serv_meta_acu = int(request.args.get('serv_meta_acu'))

    cdc_real = int(request.args.get('cdc_real'))
    cdc_meta_tot = int(request.args.get('cdc_meta_tot'))
    cdc_meta_acu = int(request.args.get('cdc_meta_acu'))

    dia = int(request.args.get('dia'))
    mes = int(request.args.get('mes'))

    fig = gerar_imagem_vc(cd_fun, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu, cdc_real, cdc_meta_tot, cdc_meta_acu, dia, mes)

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, bbox_inches='tight')
    img_bytes.seek(0)

    return Response(img_bytes, mimetype='image/png')


@app.route('/gerente/grafico_mensal', methods=['GET','POST'])
def plot_gl_mensal():
    cd_fun = 11 #int(request.args.get('cd_fun'))
    cd_fil = 1000 #int(request.args.get('cd_fil'))
    fil_porte = 3 #int(request.args.get('fil_porte'))
    fil_perfil = 111111 #int(request.args.get('fil_perfil'))

    merc_real = 555598 #int(request.args.get('merc_real'))
    merc_meta_tot = 2051190 #int(request.args.get('merc_meta_tot'))
    merc_meta_acu = 528053 #int(request.args.get('merc_meta_acu'))

    serv_real = 70420 #int(request.args.get('serv_real'))
    serv_meta_tot = 203812 #int(request.args.get('serv_meta_tot'))
    serv_meta_acu = 52587 #int(request.args.get('serv_meta_acu'))

    cdc_real = 51206 #int(request.args.get('cdc_real'))
    cdc_meta_tot = 148340 #int(request.args.get('cdc_meta_tot'))
    cdc_meta_acu = 38274 #int(request.args.get('cdc_meta_acu'))

    moveis_real = 40615 #int(request.args.get('moveis_real'))
    moveis_meta_tot = 159469 #int(request.args.get('moveis_meta_tot'))
    moveis_meta_acu = 41109 #int(request.args.get('moveis_meta_acu'))

    port_real = 20827 #int(request.args.get('port_real'))
    port_meta_tot = 70409 #int(request.args.get('port_meta_tot'))
    port_meta_acu = 17983 #int(request.args.get('port_meta_acu'))

    cartao_real = 10 #int(request.args.get('cartao_real'))
    cartao_meta_tot = 118 #int(request.args.get('cartao_meta_tot'))
    cartao_meta_acu = 14 #int(request.args.get('cartao_meta_acu'))

    fam_serv = 1 #int(request.args.get('fam_serv'))
    nps_real = 72 #int(request.args.get('nps_real'))
    nps_meta_tot = 90 #int(request.args.get('nps_meta_tot'))

    dia = 12 #int(request.args.get('dia'))
    mes = 3 #int(request.args.get('mes'))

    fig = gerar_imagem_glm(cd_fun, cd_fil, fil_porte, fil_perfil, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu, cdc_real, cdc_meta_tot, cdc_meta_acu,
    moveis_real, moveis_meta_tot, moveis_meta_acu, port_real, port_meta_tot, port_meta_acu, cartao_real, cartao_meta_tot, cartao_meta_acu, fam_serv, nps_real, nps_meta_tot, dia, mes)

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, bbox_inches='tight')
    img_bytes.seek(0)

    return Response(img_bytes, mimetype='image/png')


@app.route('/vendedorlider/grafico_categ', methods=['GET','POST'])
def plot_vl_categ():
    cd_fun = int(request.args.get('cd_fun'))
    cd_fil = int(request.args.get('cd_fil'))

    merc_real = int(request.args.get('merc_real'))
    merc_meta_tot = int(request.args.get('merc_meta_tot'))
    merc_meta_acu = int(request.args.get('merc_meta_acu'))

    serv_real = int(request.args.get('serv_real'))
    serv_meta_tot = int(request.args.get('serv_meta_tot'))
    serv_meta_acu = int(request.args.get('serv_meta_acu'))

    cdc_real = int(request.args.get('cdc_real'))
    cdc_meta_tot = int(request.args.get('cdc_meta_tot'))
    cdc_meta_acu = int(request.args.get('cdc_meta_acu'))

    dia = int(request.args.get('dia'))
    mes = int(request.args.get('mes'))

    fig = gerar_imagem_vl_categ(cd_fun, cd_fil, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu,
    cdc_real, cdc_meta_tot, cdc_meta_acu, dia, mes)

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, bbox_inches='tight')
    img_bytes.seek(0)

    return Response(img_bytes, mimetype='image/png')


@app.route('/vendedorlider/grafico_loja', methods=['GET','POST'])
def plot_vl_loja():
    cd_fun = int(request.args.get('cd_fun'))
    cd_fil = int(request.args.get('cd_fil'))
    fil_perfil = int(request.args.get('fil_perfil'))

    merc_real = int(request.args.get('merc_real'))
    merc_meta_tot = int(request.args.get('merc_meta_tot'))
    merc_meta_acu = int(request.args.get('merc_meta_acu'))

    serv_real = int(request.args.get('serv_real'))
    serv_meta_tot = int(request.args.get('serv_meta_tot'))
    serv_meta_acu = int(request.args.get('serv_meta_acu'))

    cdc_real = int(request.args.get('cdc_real'))
    cdc_meta_tot = int(request.args.get('cdc_meta_tot'))
    cdc_meta_acu = int(request.args.get('cdc_meta_acu'))

    moveis_real = int(request.args.get('moveis_real'))
    moveis_meta_tot = int(request.args.get('moveis_meta_tot'))
    moveis_meta_acu = int(request.args.get('moveis_meta_acu'))

    port_real = int(request.args.get('port_real'))
    port_meta_tot = int(request.args.get('port_meta_tot'))
    port_meta_acu = int(request.args.get('port_meta_acu'))

    cartao_real = int(request.args.get('cartao_real'))
    cartao_meta_tot = int(request.args.get('cartao_meta_tot'))
    cartao_meta_acu = int(request.args.get('cartao_meta_acu'))

    fam_serv = int(request.args.get('fam_serv'))
    nps_real = int(request.args.get('nps_real'))
    nps_meta_tot = int(request.args.get('nps_meta_tot'))

    dia = int(request.args.get('dia'))
    mes = int(request.args.get('mes'))

    fig = gerar_imagem_vl_loja(cd_fun, cd_fil, fil_perfil, merc_real, merc_meta_tot, merc_meta_acu, serv_real, serv_meta_tot, serv_meta_acu, cdc_real, cdc_meta_tot, cdc_meta_acu,
    moveis_real, moveis_meta_tot, moveis_meta_acu, port_real, port_meta_tot, port_meta_acu, cartao_real, cartao_meta_tot, cartao_meta_acu, fam_serv, nps_real, nps_meta_tot, dia, mes)

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, bbox_inches='tight')
    img_bytes.seek(0)

    return Response(img_bytes, mimetype='image/png')