# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'

    name = fields.Char(string="Title(first column)", required=True, help="Name of Course")
    description = fields.Text()

    # у каждого курса есть только один учитель(пусть он будет ответсвенный за курс).
    # разные курсы(биологию, химию) может вести ТОЛЬКО ОДИН учитель, поэтмоу берем его с табл res.users как Many2one
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible id(person/teacher) of course", index=True)

    # первичный ключ - это курс(предмет), который может иметь много сессий
    # One2many is a virtual relationship, there must be a Many2one field in the other_model,
    # т.е. мы в классе Курса и смотрим с ее перпективы: у одного курса(химии) может быть много сессий(2019,2020) -
    # поэтому нужно указывать конкретную сессию(их много)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    # Add sql restrains
    # 1)CHECK that the course description and the course title are different
    # 2)Make the Course’s name UNIQUE
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),  # http://i.imgur.com/8C1gKde.png

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),  # http://i.imgur.com/ikRt1XC.png
    ]

    def copy(self, default=None):
        """в случае копирования курса падает ошибка http://i.imgur.com/KfGHmoX.png из-за _sql_constraints на уникальное
         имя, поэтмоу создадим метод http://i.imgur.com/RSG0kOk.png"""
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])  # для счеткика, если уже есть имя с "Copy of {}..."
        # например Copy of course, Copy of course(1) ... - для подсчета уже созданных копий
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)  # используем метод супер, что бы сказать классу  Course использовать
        # именно этот метод copy, а не встроенный в него метод copy по умолчанию


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    # у каждой сессии(прошлой,нынешный, следующие, паралелльной - many)  может быть только один ответсвенный за
    # ее проведения(ректор), а если новый  ректор, то у него будет свои сессии, но ректор ТОЛЬКО ОДИН поэтмоу Many2one
    instructor_id = fields.Many2one('res.partner', string="Instructor")

    # вторичный ключ(для определения множества уникальных курсов/предметов за одну сессию)
    # т.е "Many" уникальных обьектов(курсов/предметов/course_id) могут относиться к одной сессии только "One" раз
    # т.е. мы в классе Сессии и смотрим с ее перпективы: может быть много сессий(2019,2020) у одного курса(химии)
    # мы можем подтянуть за один обьект сессии  много-"Many" уникальных-"One" курсов/предметов
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)

    # primary_key in course-model and foreign_key in Session-model
    # -----------------------------------------------------------------------------------------------------------------
    #                   Course                            |                  Session
    # course_id 'name','description','responsible_id'     |session_id  'name'    'start_date','duration','course_id'
    #  1 'химия','что-то про химию','И.И.Иваныч'},        |   1     'сесиия2019', 14.03.2019,    30,        1
    #  2 'биология', 'что-то про биологию, 'П.П.Петров'   |   2     'сесиия2019', 14.03.2019,    30,        2
    #  3 'физика', 'что-то про физику, 'Ж.Ж.Жановна'      |   3     'сесиия2019', 14.03.2019,    30,        3
    #  4 'матан', 'что-то про матан, 'П.П.Петров'         |   4     'сессиия2020' 22.09.2020,    28,        1
    #  -----------------------------------------------------------------------------------------------------------

    # т.е. когда мы хотим добавить много  полей к нашей таблице(http://i.imgur.com/03ipjtE.png) из другой таблицы
    # используем М2М, когда хотим всего одного(http://i.imgur.com/hlvbhBY.png) - М2О
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')  # используется для подсчета на лету(не создавая запись в бд) новых полей, на основе полученных данных
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')  # используют для перерасчета существющих полей, при изменение значении
    # одного из и оно будет будет исполняться автоматичекси(ненужно нигде укзывать) http://i.imgur.com/Q6K195a.png
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

    @api.constrains('instructor_id', 'attendee_ids')  # - add restrain http://i.imgur.com/tiLfJU9.png
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:  # первое условие проверяет что вообще существует иснтурктор, а второй - наличие его в посещаемых
                raise exceptions.ValidationError("A session's instructor can't be an attendee")





