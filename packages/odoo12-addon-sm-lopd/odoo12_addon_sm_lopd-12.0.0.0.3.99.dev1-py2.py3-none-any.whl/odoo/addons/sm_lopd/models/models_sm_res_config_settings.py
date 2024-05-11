# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lopd_mail_template_id = fields.Many2one(
        related='company_id.lopd_mail_template_id',
        string=_("LOPD notification template"),
        readonly=False)

    lopd_company_mail_template_id = fields.Many2one(
        related='company_id.lopd_company_mail_template_id',
        string=_("LOPD company notification template"),
        readonly=False)
