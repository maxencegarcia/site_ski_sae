#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_ski = Blueprint('admin_declinaison_ski', __name__,
                         template_folder='templates')


@admin_declinaison_ski.route('/admin/declinaison_ski/add')
def add_declinaison_ski():
    id_ski=request.args.get('id_ski')
    mycursor = get_db().cursor()
    ski=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/ski/add_declinaison_ski.html'
                           , ski=ski
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_ski.route('/admin/declinaison_ski/add', methods=['POST'])
def valid_add_declinaison_ski():
    mycursor = get_db().cursor()

    id_ski = request.form.get('id_ski')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/ski/edit?id_ski=' + id_ski)


@admin_declinaison_ski.route('/admin/declinaison_ski/edit', methods=['GET'])
def edit_declinaison_ski():
    id_declinaison_ski = request.args.get('id_declinaison_ski')
    mycursor = get_db().cursor()
    declinaison_ski=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/ski/edit_declinaison_ski.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_ski=declinaison_ski
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_ski.route('/admin/declinaison_ski/edit', methods=['POST'])
def valid_edit_declinaison_ski():
    id_declinaison_ski = request.form.get('id_declinaison_ski','')
    id_ski = request.form.get('id_ski','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_ski modifié , id:' + str(id_declinaison_ski) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/ski/edit?id_ski=' + str(id_ski))


@admin_declinaison_ski.route('/admin/declinaison_ski/delete', methods=['GET'])
def admin_delete_declinaison_ski():
    id_declinaison_ski = request.args.get('id_declinaison_ski','')
    id_ski = request.args.get('id_ski','')

    flash(u'declinaison supprimée, id_declinaison_ski : ' + str(id_declinaison_ski),  'alert-success')
    return redirect('/admin/ski/edit?id_ski=' + str(id_ski))
