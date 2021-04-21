# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from my_addons.instagram.instascraper import *


class Instagram(http.Controller):
    @http.route('/instpost_webform', type="http", auth="public", website=True)
    def instpost_webform(self, **kw):
        """здесь мы можем предварительно брать данные с базы и брасать их в наш шаблок перед редиректом по роуту"""
        # print("Execution Here.........................", kw)
        # doctor_rec = request.env['hospital.doctor'].sudo().search([])
        # print("doctor_rec...", doctor_rec)
        return http.request.render('instagram.get_info_post', {"qty_posts": 3})

    @http.route('/create/webposts', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):
        """здесь мы получаем данные с темплейта, их обрабатываем и передаем дальше"""
        print("Data Received.....", kw)

        request.env['instagram.instagram'].sudo().create(kw)


        # doctor_val = {
        #     'name': kw.get('patient_name')
        # }
        # request.env['hospital.doctor'].sudo().create(doctor_val)
        return request.render("instagram.success_msg_and_data", {})