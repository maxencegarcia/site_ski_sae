#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Correction : Récupérer les vraies infos du client
    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()  # Récupère la ligne de l'utilisateur

    return render_template('client/coordonnee/show_coordonnee.html', utilisateur=utilisateur)


@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Correction : On va chercher les données pour pré-remplir le formulaire
    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html', utilisateur=utilisateur)


@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Récupération des données du formulaire HTML
    nom = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    # --- AJOUT DU SQL UPDATE ---
    sql = "UPDATE utilisateur SET nom = %s, login = %s, email = %s WHERE id_utilisateur = %s"
    mycursor.execute(sql, (nom, login, email, id_client))

    get_db().commit()  # Très important pour enregistrer dans la base !
    flash(u'Profil mis à jour avec succès', 'alert-success')

    return redirect('/client/coordonnee/show')


    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    return render_template('client/coordonnee/add_adresse.html'
                           #,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    return render_template('/client/coordonnee/edit_adresse.html'
                           # ,utilisateur=utilisateur
                           # ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    return redirect('/client/coordonnee/show')
