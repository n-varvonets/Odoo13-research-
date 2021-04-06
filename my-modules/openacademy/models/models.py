# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'   # то как найти данный класс/модель/таблицу именно для связи с бд
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)  # то как будет называться титл кусра(для различных способов отображения и поиска)
    description = fields.Text()


class Session(models.Model):  # a session is an occurrence of a course taught at a given time for a given audience
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")  # плавающей запятой: 6 - это общее количество цифр, а 2 - количество цифр после запятой. Обратите внимание, что в результате количество цифр перед запятой составляет максимум 4
    seats = fields.Integer(string="Number of seats")

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
