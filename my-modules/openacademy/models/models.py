# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ComputedModel(models.Model):
    _name = 'test.computed'

    name = fields.Char(compute='_compute_name')  # computed on-the-fly by calling a method of the model.
    value = fields.Integer()

    @api.depends('value')  # The ORM expects the developer to specify those dependencies on the compute method with the decorator depends()
    def _compute_name(self):
        for record in self:
            record.name = "Record with value %s" % record.value


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
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")  # плавающей запятой: 6 - это общее количество цифр, а 2 - количество цифр после запятой. Обратите внимание, что в результате количество цифр перед запятой составляет максимум 4
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'ilike', "Teacher")])  # domain - When selecting the instructor for a Session, only instructors (partners with instructor set to True) should be visible

    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)  # A session is related to a course; the value of that field is a record of the model openacademy.course and is required.

    attendee_ids = fields.Many2many('res.partner', string="Attendees")  # to relate every session to a set of attendees. Attendees will be represented by partner records, so we will relate to the built-in model res.partner.

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')  # Add the percentage of taken seats
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    # is used in the user interface, to automatically change some field values when other fields are changed


    #  Add an explicit onchange to warn about invalid values, like a negative number of seats, or more participants than seats.
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
