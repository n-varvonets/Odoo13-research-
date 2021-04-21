# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



# class Instagram(http.Controller):
#     @http.route('/patient_webform', type="http", auth="public", website=True)
#     def patient_webform(self, **kw):
#         print("Execution Here.........................")
#         doctor_rec = request.env['hospital.doctor'].sudo().search([])
#         print("doctor_rec...", doctor_rec)
#         return http.request.render('om_hospital.create_patient', {'patient_name': 'Odoo Mates Test 123',
#                                                                   'doctor_rec': doctor_rec})
#
#     @http.route('/create/webpatient', type="http", auth="public", website=True)
#     def create_webpatient(self, **kw):
#         print("Data Received.....", kw)
#         request.env['hospital.patient'].sudo().create(kw)
#         # doctor_val = {
#         #     'name': kw.get('patient_name')
#         # }
#         # request.env['hospital.doctor'].sudo().create(doctor_val)
#         return request.render("om_hospital.patient_thanks", {})