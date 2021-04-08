# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'

    name = fields.Char(string="Title(first column)", required=True, help="Name of Course")
    description = fields.Text()

    # у каждого курса есть только один учитель(пусть он будет ответсвенный за курс).
    # разные курсы(биологию, химию) может вести ТОЛЬКО ОДИН учитель, поэтмоу берем его с табл res.users как Many2one
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible id(person/teacher) of course", index=True)

    # много курсов могут принадлежать только одной сессии поэтому M2O, поэтмоу - мое первое умозаключение
    # но потом подумал, тут М2М - у разных(many) курсов может быть много(many) сессий (прошлый год,этот, а курс та так и есть)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    # у каждой сессии(прошлой,нынешный, следующие, паралелльной - many)  может быть только один ответсвенный за
    # ее проведения(ректор), а если новый  ректор, то у него будет свои сессии, но ректор ТОЛЬКО ОДИН поэтмоу Many2one
    instructor_id = fields.Many2one('res.partner', string="Instructor")

    # у одного курса(биология,химия - они вечны не зависимо от сессий)может быть сколько угодно сессий, поэтому Many2one
    # Т.е. получается что и у каждой одной сессии может быть сколько угодно курсов, а не только один определенный курс?
    # т.е.у меня может быть сколько ручек, а ручки как может быть только я один(условия моя личная), так и много людей(условие: публичное)
    #  ну тогда это М2М, потому что у одной сессии может быть сколько оугдно курсов, так и наоборот, но в докум так как ниже
    # (ссылается на весь обьект курса, со всеми полями/данными)
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)



