from odoo import models, fields
import datetime

class Budget(models.Model):
    _name = 'budget.management'
    _description = 'Budget Management'

    name = fields.Char(string='Name')
    id_proyek = fields.Many2one('project.management', string='ID Proyek', required=True)
    kategori_anggaran = fields.Selection([
        ('worker', 'Workers'),
        ('materials', 'Materials'),
        ('equipment', 'Equipment'),
    ], string='Category', default='draft')
    jumlah_anggaran = fields.Integer(string='Amount', readonly=True)
    tanggal_pembuatan_anggaran = fields.Date(string='Created Date', default=datetime.date.today())
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)

    