#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_ski = Blueprint('admin_type_ski', __name__,
                        template_folder='templates')

@admin_type_ski.route('/admin/type-ski/show')
def show_type_ski():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_ski = mycursor.fetchall()
    types_ski=[]
    return render_template('admin/type_ski/show_type_ski.html', types_ski=types_ski)

@admin_type_ski.route('/admin/type-ski/add', methods=['GET'])
def add_type_ski():
    return render_template('admin/type_ski/add_type_ski.html')

@admin_type_ski.route('/admin/type-ski/add', methods=['POST'])
def valid_add_type_ski():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-ski/show') #url_for('show_type_ski')

@admin_type_ski.route('/admin/type-ski/delete', methods=['GET'])
def delete_type_ski():
    id_type_ski = request.args.get('id_type_ski', '')
    mycursor = get_db().cursor()

    flash(u'suppression type ski , id : ' + id_type_ski, 'alert-success')
    return redirect('/admin/type-ski/show')

@admin_type_ski.route('/admin/type-ski/edit', methods=['GET'])
def edit_type_ski():
    id_type_ski = request.args.get('id_type_ski', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_ski,))
    type_ski = mycursor.fetchone()
    return render_template('admin/type_ski/edit_type_ski.html', type_ski=type_ski)

@admin_type_ski.route('/admin/type-ski/edit', methods=['POST'])
def valid_edit_type_ski():
    libelle = request.form['libelle']
    id_type_ski = request.form.get('id_type_ski', '')
    tuple_update = (libelle, id_type_ski)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type ski modifié, id: ' + id_type_ski + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-ski/show')








