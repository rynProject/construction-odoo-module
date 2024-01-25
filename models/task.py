from odoo import models, fields

class Task(models.Model):
    _name = 'project.task'
    _description = 'Project Task'

    id_tugas = fields.Many2one(comodel_name='project.task', string='Task')
    name = fields.Char(string='Task', required=True)
    deskripsi_tugas = fields.Text(string='Description')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_tugas = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Task Status', default='draft')
    id_proyek = fields.Many2one('project.management', string='Project')
    id_manajer_tugas = fields.Many2one('res.users', string='Task Manager', required=True)

    