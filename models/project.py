from odoo import models, fields

class Project(models.Model):
    _name = 'project.management'
    _description = 'Project Management'

    name = fields.Char(string='Project Name', required=True)
    lokasi_proyek = fields.Char(string='Location')
    anggaran_proyek = fields.Integer(string='Budget')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_proyek = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Status Proyek', default='draft')
    id_manajer_proyek = fields.Many2one('res.users', string='Project Manager', required=True)

    task_ids = fields.One2many(comodel_name='project.task', inverse_name='id_proyek', string='Task List')