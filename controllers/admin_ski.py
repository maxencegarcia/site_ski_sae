#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_ski = Blueprint('admin_ski', __name__,
                          template_folder='templates')


@admin_ski.route('/admin/ski/show')
def show_ski():
    mycursor = get_db().cursor()
    sql = '''  requête admin_ski_1
    '''
    mycursor.execute(sql)
    skis = mycursor.fetchall()
    return render_template('admin/ski/show_ski.html', skis=skis)


@admin_ski.route('/admin/ski/add', methods=['GET'])
def add_ski():
    mycursor = get_db().cursor()

    return render_template('admin/ski/add_ski.html'
                           #,types_ski=type_ski,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_ski.route('/admin/ski/add', methods=['POST'])
def valid_add_ski():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_ski_id = request.form.get('type_ski_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_ski_2 '''

    tuple_add = (nom, filename, prix, type_ski_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'ski ajouté , nom: ', nom, ' - type_ski:', type_ski_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'ski ajouté , nom:' + nom + '- type_ski:' + type_ski_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/ski/show')


@admin_ski.route('/admin/ski/delete', methods=['GET'])
def delete_ski():
    id_ski=request.args.get('id_ski')
    mycursor = get_db().cursor()
    sql = ''' requête admin_ski_3 '''
    mycursor.execute(sql, id_ski)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet ski : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_ski_4 '''
        mycursor.execute(sql, id_ski)
        ski = mycursor.fetchone()
        print(ski)
        image = ski['image']

        sql = ''' requête admin_ski_5  '''
        mycursor.execute(sql, id_ski)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un ski supprimé, id :", id_ski)
        message = u'un ski supprimé, id : ' + id_ski
        flash(message, 'alert-success')

    return redirect('/admin/ski/show')


@admin_ski.route('/admin/ski/edit', methods=['GET'])
def edit_ski():
    id_ski=request.args.get('id_ski')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_ski_6    
    '''
    mycursor.execute(sql, id_ski)
    ski = mycursor.fetchone()
    print(ski)
    sql = '''
    requête admin_ski_7
    '''
    mycursor.execute(sql)
    types_ski = mycursor.fetchall()

    # sql = '''
    # requête admin_ski_6
    # '''
    # mycursor.execute(sql, id_ski)
    # declinaisons_ski = mycursor.fetchall()

    return render_template('admin/ski/edit_ski.html'
                           ,ski=ski
                           ,types_ski=types_ski
                         #  ,declinaisons_ski=declinaisons_ski
                           )


@admin_ski.route('/admin/ski/edit', methods=['POST'])
def valid_edit_ski():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_ski = request.form.get('id_ski')
    image = request.files.get('image', '')
    type_ski_id = request.form.get('type_ski_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_ski_8
       '''
    mycursor.execute(sql, id_ski)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_ski_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_ski_id, description, id_ski))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'ski modifié , nom:' + nom + '- type_ski :' + type_ski_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/ski/show')







@admin_ski.route('/admin/ski/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    ski=[]
    commentaires = {}
    return render_template('admin/ski/show_avis.html'
                           , ski=ski
                           , commentaires=commentaires
                           )


@admin_ski.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    ski_id = request.form.get('idski', None)
    userId = request.form.get('idUser', None)

    return admin_avis(ski_id)
