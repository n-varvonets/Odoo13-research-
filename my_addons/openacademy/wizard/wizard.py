# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):   # http://i.imgur.com/nX1vWWN.png
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    """ 1)только для одной сессии - http://i.imgur.com/nX1vWWN.png """
    # def _default_session(self):
    #     return self.env['openacademy.session'].browse(self._context.get('active_id'))
    #
    # session_id = fields.Many2one('openacademy.session', string="Session", required=True, default=_default_session)
    #
    # def subscribe(self):
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     return {}

    """ 2)для всех сессий - http://i.imgur.com/4zIBLWC.png """
    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',
                                   string="Sessions(field 1)", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees(field 2)")

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids  # типо на лету добавляет второе значение к первому(append)
        return {}



