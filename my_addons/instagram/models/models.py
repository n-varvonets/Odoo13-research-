# -*- coding: utf-8 -*-
from my_addons.instagram.instascraper import *
from odoo import models, fields, api


class Instagram(models.Model):
    _name = 'instagram.instagram'
    _description = 'instagram.instagram'

    name = fields.Char(string="Instagram model", required=True)

    # username = fields.Char(string="Your username", required=True)
    # user_login = fields.Char(string="Input your email/phone for authorization in instagram", required=True)
    # user_pass = fields.Char(string="Input your password for authorization in instagram", required=True)
    # qty_posts = fields.Integer(string="Input the number of posts you want to find", default=3)
    # required_acc_to_find = fields.Char(string="Input name of instagram account who you are looking for", required=True)

    # id_post = fields.Char(string="ID of post", store=True)
    # img = fields.Char(string="URL img", store=True)

    # def _add_id(self):
    #     id_post.
