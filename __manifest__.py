# -*- coding: utf-8 -*-
{
    'name': 'InfoSaône - Recherche dans le contenu des pièces jointes pour Odoo 18',
    'version': '18.0.1.0.0',
    'category': 'InfoSaône',
    'summary': 'Permet de rechercher dans le contenu indexé des pièces jointes du chatter',
    'description': """
InfoSaône - Recherche dans le contenu des pièces jointes pour Odoo 18
=============================================

Ce module étend la recherche du chatter pour inclure le contenu indexé 
des pièces jointes (PDF, DOCX, XLSX, ODT, etc.).

Prérequis :
- Le module `attachment_indexation` doit être installé
- Pour les PDF : `apt install python3-pdfminer` ou `pip install pdfminer.six`
    """,
    'author': 'Tony Galmiche / InfoSaône',
    'depends': ['mail', 'attachment_indexation'],
    'data': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
