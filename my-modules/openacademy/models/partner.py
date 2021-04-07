# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    """Using model inheritance, modify the existing Partner model to add an instructor boolean field,
     and a many2many field that corresponds to the session-partner relation"""
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)

