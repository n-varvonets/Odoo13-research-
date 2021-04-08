# -*- coding: utf-8 -*-

from odoo import models, fields, api


class openacademy(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'

    name = fields.Char(string="Title(first column)", required=True, help="Name of Course")
    description = fields.Text()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
