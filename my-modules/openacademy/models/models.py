# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'   # то как найти данный класс/модель/таблицу именно для связи с бд
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)  # то как будет называться титл кусра(для различных способов отображения и поиска)
    description = fields.Text()

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
