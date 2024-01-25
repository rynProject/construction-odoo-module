from odoo import models, fields

class Expenditure(models.Model):
    _name = 'expenditure.management'
    _description = 'Expenditure Management'

    name = fields.Char(string='Name')
    id_proyek = fields.Many2one('project.management', string='ID Proyek', required=True)
    deskripsi_pengeluaran = fields.Text(string='Deskripsi Pengeluaran')
    jumlah_pengeluaran = fields.Float(string='Jumlah Pengeluaran')
    tanggal_pengeluaran = fields.Date(string='Tanggal Pengeluaran')
    create_uid = fields.Many2one('res.users', string='Created By', required=True)