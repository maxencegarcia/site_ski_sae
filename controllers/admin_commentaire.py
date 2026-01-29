#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/ski/commentaires', methods=['GET'])
def admin_ski_details():
    mycursor = get_db().cursor()
    id_ski =  request.args.get('id_ski', None)
    sql = '''    requête admin_type_ski_1    '''
    commentaires = {}
    sql = '''   requête admin_type_ski_1_bis   '''
    ski = []
    sql = '''   requête admin_type_ski_1_3   '''
    nb_commentaires = []
    return render_template('admin/ski/show_ski_commentaires.html'
                           , commentaires=commentaires
                           , ski=ski
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/ski/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_ski = request.form.get('id_ski', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_ski_2   '''
    tuple_delete=(id_utilisateur,id_ski,date_publication)
    get_db().commit()
    return redirect('/admin/ski/commentaires?id_ski='+id_ski)


@admin_commentaire.route('/admin/ski/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_ski = request.args.get('id_ski', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/ski/add_commentaire.html',id_utilisateur=id_utilisateur,id_ski=id_ski,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_ski = request.form.get('id_ski', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_ski_3   '''
    get_db().commit()
    return redirect('/admin/ski/commentaires?id_ski='+id_ski)


@admin_commentaire.route('/admin/ski/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_ski = request.args.get('id_ski', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_ski_4   '''
    get_db().commit()
    return redirect('/admin/ski/commentaires?id_ski='+id_ski)