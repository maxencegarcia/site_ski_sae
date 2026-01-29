#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS   '''

    mycursor.execute(sql)
    sql='''
    CREATE TABLE utilisateur(
  
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
    INSERT INTO utilisateur
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE type_ski(
    
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO type_ski
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE etat (
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ski (
    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ski (

         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande (
    ) DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_commande(
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande 
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_panier (
    );  
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
