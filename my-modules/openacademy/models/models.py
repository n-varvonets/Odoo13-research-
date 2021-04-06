# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'   # то как найти данный класс/модель/таблицу именно для связи с бд
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)  # то как будет называться титл кусра(для различных способов отображения и поиска)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True) # A course has a responsible user; the value of that field is a record of the built-in model res.user
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")


class Session(models.Model):  # a session is an occurrence of a course taught at a given time for a given audience
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")  # плавающей запятой: 6 - это общее количество цифр, а 2 - количество цифр после запятой. Обратите внимание, что в результате количество цифр перед запятой составляет максимум 4
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor")  # A session has an instructor; the value of that field is a record of the built-in model res.partner
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)  # A session is related to a course; the value of that field is a record of the model openacademy.course and is required.

    attendee_ids = fields.Many2many('res.partner', string="Attendees")  # to relate every session to a set of attendees. Attendees will be represented by partner records, so we will relate to the built-in model res.partner.

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
