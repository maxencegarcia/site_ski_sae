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
    sql='''DROP TABLE IF EXISTS ligne_panier;'''
    mycursor.execute(sql)
    sql='''
    DROP TABLE IF EXISTS ligne_commande;
    '''
    mycursor.execute(sql)
    sql=''' 
    DROP TABLE IF EXISTS commande;
    '''
    mycursor.execute(sql)

    sql=''' 
    DROP TABLE IF EXISTS ski; 
    '''
    mycursor.execute(sql)
    sql=''' 
DROP TABLE IF EXISTS utilisateur;
    '''
    mycursor.execute(sql)
    sql=''' 
DROP TABLE IF EXISTS etat;
    '''
    mycursor.execute(sql)
    sql=''' 
DROP TABLE IF EXISTS longueur;
    '''
    mycursor.execute(sql)
    sql=''' 
DROP TABLE IF EXISTS type_ski;
    '''
    mycursor.execute(sql)
    sql=''' 
DROP TABLE IF EXISTS marque;
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE type_ski (
    id_type_ski INT PRIMARY KEY AUTO_INCREMENT,
    libelle_type_ski VARCHAR(255) 
);
    '''
    mycursor.execute(sql)
    sql = ''' 
    CREATE TABLE marque (
    id_marque INT PRIMARY KEY AUTO_INCREMENT,
    libelle VARCHAR(255) 
);
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE longueur (
    id_longueur INT PRIMARY KEY AUTO_INCREMENT,
    libelle_longueur VARCHAR(255) 
);
     '''
    mycursor.execute(sql)
    sql = ''' 
    CREATE TABLE etat (
    id_etat INT PRIMARY KEY AUTO_INCREMENT,
    libelle_etat VARCHAR(255) 
);
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE utilisateur (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(50), 
    est_actif TINYINT(1)
);
     '''
    mycursor.execute(sql)
    sql = ''' 
CREATE TABLE ski (
    id_ski INT PRIMARY KEY AUTO_INCREMENT,
    nom_ski VARCHAR(255),
    largeur INT,
    prix_ski DECIMAL(10, 2),
    fournisseur VARCHAR(255),
    id_marque INT,
    conseil_utilisation TEXT,
    photo VARCHAR(255),
    stock INT DEFAULT 0,
    type_ski_id INT,
    longueur_id INT,
    FOREIGN KEY (id_marque) REFERENCES marque(id_marque),
    FOREIGN KEY (type_ski_id) REFERENCES type_ski(id_type_ski),
    FOREIGN KEY (longueur_id) REFERENCES longueur(id_longueur)
);                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande (
    id_commande INT PRIMARY KEY AUTO_INCREMENT,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    etat_id INT, 
    utilisateur_id INT,
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);
         '''
    mycursor.execute(sql)
    sql = ''' 
    CREATE TABLE ligne_commande (
    commande_id INT,
    ski_id INT,      
    quantite INT,
    PRIMARY KEY (commande_id, ski_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (ski_id) REFERENCES ski(id_ski)
);
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_panier (
    utilisateur_id INT,
    ski_id INT,      
    quantite_panier INT,
    PRIMARY KEY (utilisateur_id, ski_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (ski_id) REFERENCES ski(id_ski)
);
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO type_ski (id_type_ski, libelle_type_ski) VALUES 
(NULL, 'Mini-ski'), (2, 'Ski de fond'), (3, 'Ski de piste'), (4, 'Ski de randonnée'), (5, 'Freestyle'), (6, 'Freeride');
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO longueur (id_longueur, libelle_longueur) VALUES 
(NULL, '118'), (2, '125'), (3, '156'), (4, '165'), (5, '172'), (6, '174'), (7, '176'), (8, '177'), (9, '180'), (10, '181'), (11, '184'), (12, '205');
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO etat (id_etat, libelle_etat) VALUES 
(NULL, 'En attente'), (2, 'En préparation'), (3, 'Expédiée'), (4, 'Livrée'), (5, 'Annulée');

         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO marque (id_marque, libelle) VALUES 
(NULL, 'Wedze'), (2, 'Inovix'), (3, 'Rossignol'), (4, 'Atomic'), (5, 'Salomon'), (6, 'Dynastar'), (7, 'Elan');

         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(NULL,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(NULL,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(NULL,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ski (id_ski, nom_ski, largeur, prix_ski, fournisseur, id_marque, conseil_utilisation, photo, stock, type_ski_id, longueur_id) VALUES 
(NULL, 'Wedze 500', 80, 240, 'Decathlon', 1, 'Polyvalent', 'wedze_500.jpg', 10, 5, 5),
(NULL, 'Wedze 500 Slash 100', 100, 360, 'Decathlon', 1, 'Poudreuse', 'wedze_500_slash_100.jpg', 5, 6, 11),
(NULL, 'Inovix XC S 500', 44, 155, 'Decathlon', 2, 'Classique', 'inovix_xc_s_500.jpg', 8, 2, 12),
(NULL, 'Rossignol Experience 80', 80, 380, 'Rossignol', 3, 'All mountain', 'rossignol_experience_80.jpg', 12, 3, 6),
(NULL, 'Wedze Mountain touring MT85', 85, 575, 'Decathlon', 1, 'Randonnée légère', 'wedze_mountain_touring_mt85.jpg', 4, 4, 7),
(NULL, 'Atomic Redster X5', 70, 370, 'Atomic', 4, 'Piste performance', 'atomic_redster_x5.png', 7, 3, 8),
(NULL, 'Rossignol Experience 84', 84, 540, 'Rossignol', 3, 'Expert', 'rossignol_experience_84.png', 6, 3, 11),
(NULL, 'Salomon Max 8S', 73, 500, 'Salomon', 5, 'Slalom', 'salomon_max_8s.png', 9, 3, 4),
(NULL, 'Atomic Vantage 77 TI', 77, 420, 'Atomic', 4, 'Confort', 'atomic_vantage_77_ti.jpg', 11, 3, 3),
(NULL, 'Dynastar Vertical Deer', 85, 697, 'Dynastar', 6, 'Montagne sauvage', 'dynastar_vertical_deer.jpg', 3, 4, 9),
(NULL, 'Elan Ripstick 96', 96, 490, 'Elan', 7, 'Freeride polyvalent', 'elan_ripstick_96.jpg', 5, 6, 10),
(NULL, 'Salomon Distance M10 GW L90', 90, 299, 'Salomon', 5, 'Débutant', 'salomon_distance_m10_gw_l90.jpg', 15, 1, 2),
(NULL, 'Rossignol Freeze Xpress GW', 74, 269, 'Rossignol', 3, 'Enfant/Ado', 'rossignol_freeze_xpress_gw.jpg', 20, 1, 1);
         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
