# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date desc"

    def test_recordset(self):
        for rec in self:
            print("Odoo ORM: Record Set Operation")
            partners = self.env['res.partner'].search([])
            print("Mapped partners...", partners.mapped('email'))
            print(" Sorted partners...", partners.sorted(lambda o: o.write_date, reverse=True))
            print(" Filtered partners...", partners.filtered(lambda o: not o.customer))

    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_warning(message='Appointment is Confirmed')

    @api.model
    def create_appointment_wizard(self):
        """ Onboarding step for company basic information. """
        action = self.env.ref('om_hospital.create_appointment_wizard').read()[0]
        # action['res_id'] = self.env.user.company_id.id
        return action

    # Deleting One2Many Lines From Code and Datetime Conversion , UTC -> Local
    # https://www.youtube.com/watch?v=ZxrDGTEU7B8&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=66
    # https://www.youtube.com/watch?v=2pOIxhE_xuY&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=59
    def delete_lines(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            # print("Time in UTC -->", rec.appointment_datetime)
            # print("Time in Users Timezone -->", time_in_timezone)
            rec.appointment_lines = [(5, 0, 0)]

    # Moving the State Of the Record To Confirm State in Button Click
    # How to Add States/Statusbar for Records in Odoo
    # https://www.youtube.com/watch?v=lPHWsw3Iclk&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=21
    def action_confirm(self):
        for rec in self:
            ''' ORM - как манипулировать записями в БД, после нажатися на кнопку http://i.imgur.com/3ZqsVex.png'''
            # 1.Add to odoo search method
            patient = self.env['hospital.patient'].search(
                [])  # hospital.patient - http://i.imgur.com/RS2evIL.png, в серч вставляется домейн(условие)
            # print('patients....', patient)  # http://i.imgur.com/4mUMjkx.png
            female_patient = self.env['hospital.patient'].search([("gender", "=",
                                                                   "fe_male")])  # теперь уже с фильтром(добавить скобки для поиска цельного домена как обьекта)
            # print('female_patients....', female_patient)  # http://i.imgur.com/6sOL9AJ.png
            female_patient_40 = self.env['hospital.patient'].search([("gender", "=", "fe_male"),
                                                                     ("patient_age", ">=", "40")])
            # print('female_patients_40....', female_patient_40)  # http://i.imgur.com/DvwEXiA.png

            # 2. Add to odoo search count
            patient_count = self.env['hospital.patient'].search_count([])
            # print('patient_count....', patient_count)  # http://i.imgur.com/JAH4uA5.png

            # 3. Ref in Odoo. Получить обьект, id необходимой записи
            # Data has to be stored in DB( at least here http://i.imgur.com/kHiZNeV.png).
            om_patient = self.env.ref('om_hospital.patient_xyz')  # http://i.imgur.com/9QDG2xa.png
            # print('om_patient as obj....', om_patient, "and id is =", om_patient.id)  # http://i.imgur.com/nb6UfKv.png

            # 4. Browse. Получить конкретный обьект записи по модели и извесному его id
            browse_result = self.env['hospital.patient'].browse([200, om_patient.id])
            # browse_result = self.env['hospital.patient'].search([('id', '=', om_patient.id)])  - это тот же метод что и browse  >>>browse_result.. hospital.patient(1,)
            # print('browse_result..', browse_result)  # хоть даже  нет записи(200), то он все равно вернет обьект
            # >>> browse_result.. hospital.patient(200, 1)

            # 5. exists - Проверить существует ли запись в модели.  если хоть один есть - вернет тру
            # if browse_result.exists():
            # print('Existing')
            # else:
            # print("No existing, there is no existing record ...")

            # 6 CRUD(конечно можно определить её поведение в функции http://i.imgur.com/H8mVFJU.png,
            # но ниже примеры как сдеать с ORM - внутри кода(под капотом)

            # 6.1. Create.  для создания новой записи нужно передать все данные все необходимые данные
            vals = {
                "patient_name": 'RRRR PPPP',
                "email_id": 'asddas@gmail.com',
            }
            # self.env['hospital.patient'].create(vals)  # http://i.imgur.com/QOiLUvk.png
            created_record = self.env['hospital.patient'].create(vals)
            # print('created_record..', created_record, created_record.id, created_record.email_id)
            # >>> created_record.. hospital.patient(11,) 11 asddas@gmail.com

            # 6.2 Update existing record
            # record_to_update = self.env['hospital.patient'].browse(3)   # находим нашу запись
            # if record_to_update.exists():  # проверяем есть ли запись
            #     vals = {
            #         "patient_name": 'RRRR qqqqqqqqq',
            #         "name": 77777777777
            #     }
            #     record_to_update.write(vals)  # http://i.imgur.com/LcXx4sy.png

            # 6.3 Copy
            # record_to_copy = self.env['hospital.patient'].browse(8)
            # record_to_copy.copy()

            # 6.4 delete
            # record_to_unlink = self.env['hospital.patient'].browse(8)
            # record_to_unlink.unlink()

            # 7 name_get(display_name)
            # для создания встречи нужно взять с модуля пациент его имя и id - http://i.imgur.com/AhhXNzR.png, http://i.imgur.com/o1mJzyS.png
            # метод определения имени уже был кастомизирован(добавлен id) в http://i.imgur.com/PHeP37j.png , но если
            # закоментировать его, то айди пропадет http://i.imgur.com/uKhTU4K.png , http://i.imgur.com/2QiNdsM.png

            # мы можем получить по отдельности имя и айди записи найдя сам обьект:
            patient = self.env['hospital.patient'].search([('id', '=', 12)])
            print(patient, ',', patient.patient_name, ',', patient.name_seq)
            # >>> hospital.patient(12,) , RRRR PPPP , HP012

            # но так же есть встроенный в оду модуль display_name http://i.imgur.com/jPUlg05.png , который отобразит имя _rec_name http://i.imgur.com/gnCuC7z.png :
            # 7.а) метод name_get  отствуеет в нашем кастомном модуле
            print(
                patient.display_name)  # отображает имя http://i.imgur.com/a7YNIFX.png, хотя в модуле patient этот метод - отсутветует http://i.imgur.com/375RLk8.png и метод name_get закоменчен
            # 7.б)  метод name_get присутсвует в нашем кастомном модуле и он будет отображать любой порядок значений,
            # который мы в нем укажем например:  http://i.imgur.com/qLU6LJH.png . http://i.imgur.com/WmugFjP.png

            # 8 name_search
            # Проблема: по умолчнию поиск работает только по имени  http://i.imgur.com/t2aaeln.png.
            # Задача: добавить для поиска отсальные поля
            # Решение: добавим метод name_search в встроенную модель patient, который будет проводит поиск по заданным полям http://i.imgur.com/ZWBteP9.png
            # Результат: http://i.imgur.com/pNOUFbR.png

            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thanks You',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'draft'

    # Overriding the Create Method in Odoo
    # https://www.youtube.com/watch?v=ZfKzmfiqeg0&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=8
    @api.model
    def create(self, vals):
        # overriding the create method to add the sequence
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    # How to Override the Write Method in Odoo
    # https://www.youtube.com/watch?v=v8sXFUi1SH4&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=50
    def write(self, vals):
        # overriding the write method of appointment model
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        # do as per the need
        return res

    # Give Domain For A field dynamically in Onchange
    # How To Give Domain For A Field Based On Another Field
    # https://www.youtube.com/watch?v=IpXXYCsK2ow&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=65
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        appointment_lines = []
        product_rec = self.env['product.product'].search([])
        for pro in product_rec:
            line = (0, 0, {
                'product_id': pro.id,
                'product_qty': 1,
            })
            appointment_lines.append(line)
        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'Like and Subscribe our channel To Get Notified'
        })
        return res

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    doctor_ids = fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec',
                                  string='Doctors')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note")
    doctor_note = fields.Text(string="Note", track_visibility='onchange')
    # How to Create One2Many Field
    # https://www.youtube.com/watch?v=_O_tNBdg3HQ&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=34
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    pharmacy_note = fields.Text(string="Note", track_visibility='always')
    appointment_date = fields.Date(string='Date')
    appointment_date_end = fields.Date(string='End Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    amount = fields.Float(string="Total Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')

    product_id = fields.Many2one('product.template', string="Product Template")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                lines = [(5, 0, 0)]
                # lines = []
                print("self.product_id", self.product_id.product_variant_ids)
                for line in self.product_id.product_variant_ids:
                    val = {
                        'product_id': line.id,
                        'product_qty': 15
                    }
                    lines.append((0, 0, val))
                rec.appointment_lines = lines


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    sequence = fields.Integer(string="Sequence")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
