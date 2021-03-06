# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Instagram(models.Model):
    _name = 'instagram.instagram'
    _description = 'instagram.instagram'

    name = fields.Char(string="Instagram model")

    username = fields.Char(string="Name")
    user_login = fields.Char(string="User's email/phone", required=True)
    user_pass = fields.Char(string="User's password", required=True)
    qty_posts = fields.Integer(string="Q-ty of posts", default=3)
    required_acc_to_find = fields.Char(string="Nickname to search", required=True)

    id_post = fields.Char(string="ID of post", store=True)
    img = fields.Char(string="URL img", store=True)

    def update_post_instagram_data(self):
        print('working cron')
        # execute my code
