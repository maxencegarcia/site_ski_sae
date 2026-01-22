DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT
    login varchar(255)
    email varchar(255)
    nom varchar(255)
    password varchar(255)
    role varchar(255)
    est_actif tinyint(1)
    PRIMARY KEY id_utilisateur
)









INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'scrypt:32768:8:1$l3UTNxiLZGuBKGkg$ae3af0d19f0d16d4a495aa633a1cd31ac5ae18f98a06ace037c0f4fb228ed86a2b6abc64262316d0dac936eb72a67ae82cd4d4e4847ee0fb0b19686ee31194b3',
    'ROLE_client','client2','1');