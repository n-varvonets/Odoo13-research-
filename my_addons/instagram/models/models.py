# -*- coding: utf-8 -*-
from my_addons.instagram.instascraper import *
from odoo import models, fields, api


class instagram(models.Model):
    _name = 'instagram.instagram'
    _description = 'instagram.instagram'

    name = fields.Char()
    id_post = fields.Char(compute="_add_id", store=True)
    img = fields.Char(compute="_add_img", store=True)

    # def _add_id(self):
    #     id_post.
