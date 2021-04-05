# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()
    biography = fields.Html()

    """Также должна быть возможность создавать новые курсы прямо со страницы учителя или видеть все курсы,
         которые они преподают, поэтому добавьте обратную зависимость к модели учителя:"""
    course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")


class Courses(models.Model):
    """У каждого курса должно быть поле учитель, связанное с одной записью учителя,
        но каждый учитель может вести несколько курсов"""
    _name = 'academy.courses'
    _inherit = 'mail.thread'

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")


# class academy(models.Model):
#     _name = 'academy.academy'
#     _description = 'academy.academy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
