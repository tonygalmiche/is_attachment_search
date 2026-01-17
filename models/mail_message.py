# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.osv import expression


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _message_fetch(self, domain, search_term=None, before=None, after=None, around=None, limit=30):
        """Étend la recherche pour inclure le contenu indexé des pièces jointes."""
        res = {}
        if search_term:
            # On remplace les espaces par % pour éviter les correspondances strictes
            search_term = search_term.replace(" ", "%")
            domain = expression.AND([domain, expression.OR([
                # Recherche par nom de pièce jointe
                [("attachment_ids", "in", self.env["ir.attachment"].sudo()._search([
                    ("name", "ilike", search_term)
                ]))],
                # Recherche par contenu indexé de la pièce jointe
                [("attachment_ids", "in", self.env["ir.attachment"].sudo()._search([
                    ("index_content", "ilike", search_term)
                ]))],
                # Recherche dans le corps du message
                [("body", "ilike", search_term)],
                # Recherche dans le sujet
                [("subject", "ilike", search_term)],
                # Recherche dans la description du sous-type
                [("subtype_id.description", "ilike", search_term)],
            ])])
            res["count"] = self.search_count(domain)
        
        if around is not None:
            messages_before = self.search(
                domain=[*domain, ('id', '<=', around)],
                limit=limit // 2,
                order="id DESC"
            )
            messages_after = self.search(
                domain=[*domain, ('id', '>', around)],
                limit=limit // 2,
                order='id ASC'
            )
            return {**res, "messages": (messages_after + messages_before).sorted('id', reverse=True)}
        
        if before:
            domain = expression.AND([domain, [('id', '<', before)]])
        if after:
            domain = expression.AND([domain, [('id', '>', after)]])
        
        res["messages"] = self.search(domain, limit=limit, order='id ASC' if after else 'id DESC')
        if after:
            res["messages"] = res["messages"].sorted('id', reverse=True)
        return res
