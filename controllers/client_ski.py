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
    # utilisation du filtre
    sql = '''
            SELECT id_type_ski, libelle_type_ski AS libelle            
            FROM type_ski
            ORDER BY libelle_type_ski
            '''
    mycursor.execute(sql)
    types_ski = mycursor.fetchall()

    if 'filter_types' in session or 'filter_word' in session or 'filter_prix_min' in session or 'filter_prix_max' in session:
        sql = '''
            SELECT id_ski AS id_ski
                   , nom_ski AS nom
                   , prix_ski AS prix
                   , stock AS stock
                   , photo AS image
            FROM ski
            '''
        list_param = []
        condition_and = []
        
        if 'filter_types' in session and len(session['filter_types']) > 0:
            sql += " JOIN type_ski ON ski.type_ski_id = type_ski.id_type_ski "
            # Conversion des identifiants en entiers
            ids = tuple([int(x) for x in session['filter_types']])
            # Gestion du cas d'un seul élément pour le tuple SQL
            condition_and.append("type_ski_id IN %s")
            list_param.append(ids)
        
        if 'filter_word' in session:
            condition_and.append("nom_ski LIKE %s")
            list_param.append(f"%{session['filter_word']}%")

        if 'filter_prix_min' in session:
            condition_and.append("prix_ski >= %s")
            list_param.append(float(session['filter_prix_min']))
            
        if 'filter_prix_max' in session:
            condition_and.append("prix_ski <= %s")
            list_param.append(float(session['filter_prix_max']))
            
        if len(condition_and) > 0:
            sql += " WHERE " + " AND ".join(condition_and)

        sql += " ORDER BY nom_ski;"
        
        mycursor.execute(sql, tuple(list_param))
        ski = mycursor.fetchall()
    else:
        ski = skis
    
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
