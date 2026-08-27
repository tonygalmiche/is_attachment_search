# is_attachment_search

Étend la recherche du chatter (et la recherche sur les fiches partenaires)
pour inclure le **contenu indexé des pièces jointes** (PDF, DOCX, XLSX,
ODT, etc.), en plus du corps des messages et du nom des fichiers.

## Prérequis

- Le module `attachment_indexation` doit être installé (fournit le champ
  `index_content` sur `ir.attachment`).
- Pour l'indexation des PDF : `apt install python3-pdfminer` ou
  `pip install pdfminer.six`.

## Fonctionnement

- **Recherche dans le chatter** (`mail_message.py`) : la barre de
  recherche du chatter cherche désormais aussi dans le nom des pièces
  jointes et leur contenu indexé, en plus du corps des messages, du sujet
  et de la description du sous-type.
- **Champ de recherche générique** (`mail_thread.py`) : ajoute un champ
  calculé/recherchable `is_attachment_content` sur `mail.thread` (donc sur
  tout modèle qui hérite de ce mixin — partenaires, factures, projets...),
  qui retrouve les enregistrements dont une pièce jointe (directement liée
  ou attachée à un message du chatter) contient le texte recherché.
- **Vue de recherche** (`res_partner_views.xml`) : ajoute ce champ
  "Contenu pièces jointes" à la recherche des contacts, à titre d'exemple
  d'utilisation — le champ `is_attachment_content` reste disponible pour
  être ajouté à la recherche de n'importe quel autre modèle héritant de
  `mail.thread`.

## Limites

- La recherche par contenu ne fonctionne que sur les pièces jointes déjà
  indexées par `attachment_indexation` (indexation asynchrone à
  l'upload — un document tout juste ajouté peut ne pas être immédiatement
  cherchable).
- Les recherches passent par `sudo()` sur `ir.attachment` pour retrouver
  les correspondances de contenu, indépendamment des droits d'accès de
  l'utilisateur sur les pièces jointes elles-mêmes.
