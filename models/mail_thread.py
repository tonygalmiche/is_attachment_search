# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    is_attachment_content = fields.Char(
        string='Contenu des pièces jointes',
        compute='_compute_attachment_content',
        search='_search_attachment_content',
        help="Permet de rechercher dans le contenu indexé des pièces jointes"
    )

    def _compute_attachment_content(self):
        """Champ technique, pas besoin de valeur affichée."""
        for record in self:
            record.is_attachment_content = False

    @api.model
    def _search_attachment_content(self, operator, value):
        """Recherche les enregistrements ayant des pièces jointes avec ce contenu."""
        if operator not in ('ilike', 'like', '=', '!=', 'not ilike', 'not like'):
            return [('id', '=', False)]
        
        model_name = self._name
        
        # Recherche les pièces jointes directement liées au modèle
        attachments_direct = self.env['ir.attachment'].sudo().search([
            ('index_content', operator, value),
            ('res_model', '=', model_name),
        ])
        record_ids_direct = set(attachments_direct.mapped('res_id'))
        
        # Recherche les pièces jointes liées via mail.message
        attachments_msg = self.env['ir.attachment'].sudo().search([
            ('index_content', operator, value),
            ('res_model', '=', 'mail.message'),
        ])
        
        record_ids_msg = set()
        if attachments_msg:
            messages = self.env['mail.message'].sudo().search([
                ('attachment_ids', 'in', attachments_msg.ids),
                ('model', '=', model_name),
            ])
            record_ids_msg = set(messages.mapped('res_id'))
        
        record_ids = record_ids_direct | record_ids_msg
        
        if operator in ('!=', 'not ilike', 'not like'):
            return [('id', 'not in', list(record_ids))]
        return [('id', 'in', list(record_ids))]
