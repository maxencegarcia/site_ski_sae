#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

auth_security = Blueprint('auth_security', __name__,
                        template_folder='templates')


@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')

    # récupération de l'utilisateur
    sql = "SELECT login, role, id_utilisateur, password FROM utilisateur WHERE login=%s;"
    mycursor.execute(sql, (login,))
    user = mycursor.fetchone()

    if user:
        mdp_ok = check_password_hash(user['password'], password)
        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/login')
        else:
            session['login'] = user['login']
            session['role'] = user['role']
            session['id_user'] = user['id_utilisateur']

            if user['role'] == 'ROLE_admin':
                return redirect('/admin/commande/index')
            else:
                return redirect('/client/ski/show')
    else:
        flash(u'Vérifier votre login et essayer encore.', 'alert-warning')
        return redirect('/login')


@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    login = request.form.get('login')
    password = request.form.get('password')

    # vérifier si login ou email existe déjà
    sql = "SELECT * FROM utilisateur WHERE login=%s OR email=%s;"
    mycursor.execute(sql, (login, email))
    user = mycursor.fetchone()

    if user:
        flash(u'Votre adresse email ou votre login existe déjà', 'alert-warning')
        return redirect('/signup')

    # hash du mot de passe (consigne du prof)
    password = generate_password_hash(password, method='scrypt')

    # insertion du nouvel utilisateur
    sql = """INSERT INTO utilisateur (login, email, password, role, est_actif)
             VALUES (%s, %s, %s, %s, 1);"""
    mycursor.execute(sql, (login, email, password, 'ROLE_client'))
    get_db().commit()

    # récupérer l'id du nouvel utilisateur
    sql = "SELECT last_insert_id() AS last_insert_id;"
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    id_user = info_last_id['last_insert_id']

    # connexion automatique
    session['login'] = login
    session['role'] = 'ROLE_client'
    session['id_user'] = id_user

    return redirect('/client/ski/show')


@auth_security.route('/logout')
def auth_logout():
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    return redirect('/')


@auth_security.route('/forget-password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')
