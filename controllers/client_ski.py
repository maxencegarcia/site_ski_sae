#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_ski = Blueprint('client_ski', __name__,
                        template_folder='templates')

@client_ski.route('/client/index')
@client_ski.route('/client/ski/show')              # remplace /client
def client_ski_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
            SELECT id_ski AS id_ski
                   , nom_ski AS nom
                   , prix_ski AS prix
                   , stock AS stock
                   , photo AS image
            FROM ski
            ORDER BY nom_ski;
            '''
    mycursor.execute(sql)
    skis = mycursor.fetchall()
    ski = skis
    # list_param = []
    # condition_and = ""
    # utilisation du filtre
    sql = '''
            SELECT id_marque  AS id_type_ski
                    ,libelle            
            FROM marque
            ORDER BY  libelle
            '''
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    types_ski = marques

    sql = "SELECT * , 10 as prix , concat('nomski',ski_id) as nom FROM ligne_panier"
    mycursor.execute(sql)
    ski_panier = mycursor.fetchall()


    if len(ski_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_ski.html'
                           , ski=ski
                           , ski_panier=ski_panier
                           , prix_total=prix_total
                           , items_filtre=types_ski
                           )
