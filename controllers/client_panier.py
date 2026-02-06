#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ski = request.form.get('id_ski')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_ski=request.form.get('id_declinaison_ski',None)
    id_declinaison_ski = 1

# ajout dans le panier d'une déclinaison d'un ski (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_ski))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_ski = declinaisons[0]['id_declinaison_ski']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_ski))
    #     ski = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_ski.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , ski=ski)

# ajout dans le panier d'un ski


    return redirect('/client/ski/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ski = request.form.get('id_ski','')
    quantite = request.form.get(quantite)

    # ---------
    # partie 2 : on supprime une déclinaison de l'ski
    # id_declinaison_ski = request.form.get('id_declinaison_ski', None)

    sql = ''' SELECT * FROM ligne_panier WHERE ski_id = %s AND utilisateur_id=%s'''
    mycursor.execute(sql, (id_ski, id_client))
    ski_panier=mycursor.fetchone()

    if not(ski_panier is None) and ski_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_ski)
        sql = ''' UPDATE ligne_panier SET quantite+%s WHERE utilisateur_id =%s AND ski_id=%s'''
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_ski, quantite)
        sql = ''' INSERT INTO ligne_panier(utilisateur_id, ski_id,quantite,date_ajout) VALUES (%s,%s,%s, current_timestamp)'''
        mycursor.execute(sql, tuple_insert)

    # mise à jour du stock de l'ski disponible
    get_db().commit()
    return redirect('/client/ski/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'ski pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'ski : stock = stock + qté de la ligne pour l'ski'''
        get_db().commit()
    return redirect('/client/ski/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_ski = request.form.get('id_declinaison_ski')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'ski : stock = stock + qté de la ligne pour l'ski'''

    get_db().commit()
    return redirect('/client/ski/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            filter_word = filter_word.strip()
            if len(filter_word) > 1:
                session['filter_word'] = filter_word
            else:
                session.pop('filter_word', None)
        else:
            session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isnumeric():
            session['filter_prix_min'] = filter_prix_min
        else:
            session.pop('filter_prix_min', None)
        if filter_prix_max.isnumeric():
            session['filter_prix_max'] = filter_prix_max
        else:
            session.pop('filter_prix_max', None)
    
    if filter_types:
        session['filter_types'] = filter_types
    else:
        session['filter_types'] = []
    
    return redirect('/client/ski/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_types', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    print("suppr filtre")
    return redirect('/client/ski/show')
