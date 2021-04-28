# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



class Instagram(http.Controller):
    @http.route('/instpost_webform', type="http", auth="public", website=True)
    def instpost_webform(self, **kw):
        # print("Execution Here.........................", kw)
        # doctor_rec = request.env['hospital.doctor'].sudo().search([])
        # print("doctor_rec...", doctor_rec)
        return http.request.render('instagram.get_info_post', {"qty_posts": 3})

    @http.route('/create/webposts', type="http", auth="public", website=True)
    def create_webpatient(self, **kw):

        print("Data Received.....", kw)

        record = request.env['instagram.instagram'].sudo().create(kw)
        # om_patient = request.env.ref('om_hospital.patient_xyz')
        # browse_result = request.env['hospital.patient'].browse([200, om_patient.id])
        print('good')
        # print(request.env['instagram.instagram'].sudo().search([]))

        # print('good')
        # doctor_rec = request.env['instagram.instagram'].sudo().search(['post_data'])
        # print(doctor_rec)
        return request.render("instagram.success_msg_and_data", {})