#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/show')
def client_panier_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT lp.ski_id AS id_ski,
           s.nom_ski AS nom,
           s.prix_ski AS prix,
           s.stock,
           lp.quantite_panier AS quantite
    FROM ligne_panier lp
    JOIN ski s ON s.id_ski = lp.ski_id
    WHERE lp.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    skis_panier = mycursor.fetchall()

    prix_total = 0
    for item in skis_panier:
        prix_total += item['prix'] * item['quantite']

    return render_template('client/boutique/panier.html',
                           skis_panier=skis_panier,
                           prix_total=prix_total)


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ski = request.form.get('id_ski', type=int)
    quantite = request.form.get('quantite', type=int)

    sql = '''SELECT quantite_panier 
             FROM ligne_panier 
             WHERE utilisateur_id = %s AND ski_id = %s'''
    mycursor.execute(sql, (id_client, id_ski))
    ligne = mycursor.fetchone()

    if ligne is not None:
        sql = '''UPDATE ligne_panier 
                 SET quantite_panier = quantite_panier + %s 
                 WHERE utilisateur_id = %s AND ski_id = %s'''
        mycursor.execute(sql, (quantite, id_client, id_ski))
    else:
        sql = '''INSERT INTO ligne_panier(utilisateur_id, ski_id, quantite_panier)
                 VALUES (%s, %s, %s)'''
        mycursor.execute(sql, (id_client, id_ski, quantite))

    #sql = '''UPDATE ski SET stock = stock - %s WHERE id_ski = %s'''
    #mycursor.execute(sql, (quantite, id_ski))

    get_db().commit()
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ski = request.form.get('id_ski', type=int)

    sql = '''SELECT quantite_panier 
             FROM ligne_panier 
             WHERE utilisateur_id = %s AND ski_id = %s'''
    mycursor.execute(sql, (id_client, id_ski))
    ligne = mycursor.fetchone()

    if ligne is not None:
        if ligne['quantite_panier'] > 1:
            sql = '''UPDATE ligne_panier 
                     SET quantite_panier = quantite_panier - 1 
                     WHERE utilisateur_id = %s AND ski_id = %s'''
            mycursor.execute(sql, (id_client, id_ski))
        else:
            sql = '''DELETE FROM ligne_panier 
                     WHERE utilisateur_id = %s AND ski_id = %s'''
            mycursor.execute(sql, (id_client, id_ski))

        #sql = '''UPDATE ski SET stock = stock + 1 WHERE id_ski = %s'''
        #mycursor.execute(sql, (id_ski,))

    get_db().commit()
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT ski_id, quantite_panier 
             FROM ligne_panier 
             WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    lignes = mycursor.fetchall()

    #for ligne in lignes:
     #   sql = '''UPDATE ski
      #           SET stock = stock + %s
       #          WHERE id_ski = %s'''
        #mycursor.execute(sql, (ligne['quantite_panier'], ligne['ski_id']))

    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))

    get_db().commit()
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_ski = request.form.get('id_ski', type=int)

    sql = '''SELECT quantite_panier 
             FROM ligne_panier 
             WHERE utilisateur_id = %s AND ski_id = %s'''
    mycursor.execute(sql, (id_client, id_ski))
    ligne = mycursor.fetchone()

    if ligne is not None:
        quantite = ligne['quantite_panier']

        sql = '''DELETE FROM ligne_panier 
                 WHERE utilisateur_id = %s AND ski_id = %s'''
        mycursor.execute(sql, (id_client, id_ski))

        #sql = '''UPDATE ski
         #        SET stock = stock + %s
          #       WHERE id_ski = %s'''
        #mycursor.execute(sql, (quantite, id_ski))

    get_db().commit()
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/valider', methods=['POST'])
def client_panier_valider():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # 1. Créer la commande
    sql = '''
        INSERT INTO commande(utilisateur_id, etat_id)
        VALUES (%s, 1)
    '''
    mycursor.execute(sql, (id_client,))
    id_commande = mycursor.lastrowid

    # 2. Récupérer les lignes du panier
    sql = '''
        SELECT * FROM ligne_panier
        WHERE utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    lignes = mycursor.fetchall()

    # 3. Copier dans ligne_commande et réduire le stock
    for ligne in lignes:
        sql = '''
            INSERT INTO ligne_commande(commande_id, ski_id, quantite)
            VALUES (%s, %s, %s)
        '''
        mycursor.execute(sql, (
            id_commande,
            ligne['ski_id'],
            ligne['quantite_panier']
        ))

        sql = '''
            UPDATE ski
            SET stock = stock - %s
            WHERE id_ski = %s
        '''
        mycursor.execute(sql, (
            ligne['quantite_panier'],
            ligne['ski_id']
        ))

    # 4. Vider le panier
    sql = '''
        DELETE FROM ligne_panier
        WHERE utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))

    get_db().commit()
    return redirect('/client/panier/show')
