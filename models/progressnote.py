from odoo import models, fields

class ProgressNote(models.Model):
    _name = 'construction.progress'
    _description = 'Progress Note'

    name = fields.Char(string='Name', required=True)
    id_proyek = fields.Many2one('construction.project', string='ID Proyek', required=True)
    catatan_kemajuan = fields.Text(string='Catatan Kemajuan')
    tanggal_pembuatan_catatan = fields.Date(string='Tanggal Pembuatan Catatan')
    create_uid = fields.Many2one('res.users', string='Created By', required=True)