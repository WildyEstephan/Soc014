# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import base64
import xlwt
from io import BytesIO
from xlrd import open_workbook
import xlrd
from odoo import exceptions, _


class Tema(models.Model):
    _name = 'soc.tema'
    _description = 'Tema'

    name = fields.Char(
        string='Tema',
        required=False)
    alumno_ids = fields.Many2many(
        comodel_name='res.users',
        string='Alumno_ids')
    lleno = fields.Boolean(
        string='Lleno',
        required=False)
    cuenta_alumno = fields.Integer(
        string='Cuenta_alumno',
        required=False, compute='_compute_cuenta_alumno', store=True)

    @api.multi
    @api.depends('alumno_ids')
    def _compute_cuenta_alumno(self):
        for rec in self:
            rec.cuenta_alumno = len(rec.alumno_ids)

    def seleccionar(self):

        if self.env.user.selecciono:
            raise exceptions.UserError(("No puedes seleccionar mas de un tema"))

        alumnos = []

        if self.alumno_ids:
            for alumno in self.alumno_ids:
                alumnos.append([4,alumno.id])

            alumnos.append([4, self.env.user.id])
        else:
            alumnos.append([4, self.env.user.id])

        self.sudo().env.user.selecciono = True

        self.alumno_ids = alumnos

class ResUsers(models.Model):
    _inherit = 'res.users'

    selecciono = fields.Boolean(
        string='Selecciono',
        required=False)



