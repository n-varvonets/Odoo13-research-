# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



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
        # try:
        # posts_img_id = get_posts_data(**kw)
        # print(posts_img_id)
        #     # request.env['instagram.instagram'].sudo().create(kw)
        # except Exception as e:
        #     print(e)

        # kw = {'user_login': 'nickolay.varvonets@gmail.com', 'user_pass': "Varvonets16", 'qty_posts': '3', 'required_acc_to_find': "varan_dimode"}

        login_val = {
            'user_login': kw.get('user_login'),
            'user_pass': kw.get('user_pass'),
            'qty_posts': kw.get('qty_posts'),
            'required_acc_to_find': kw.get('required_acc_to_find'),
        }
        record = request.env['instagram.instagram'].sudo().create(kw)
        om_patient = request.env.ref('om_hospital.patient_xyz')
        browse_result = request.env['hospital.patient'].browse([200, om_patient.id])
        print('good')
        print(request.env['instagram.instagram'].sudo().search([]))

        # print('good')
        # doctor_rec = request.env['instagram.instagram'].sudo().search(['post_data'])
        # print(doctor_rec)
        return request.render("instagram.success_msg_and_data", {})