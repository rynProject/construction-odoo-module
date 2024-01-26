from odoo import models, fields

class Task(models.Model):
    _name = 'construction.task'
    _description = 'Project Task'

    name = fields.Char(string='Task', required=True)
    deskripsi_tugas = fields.Text(string='Description')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_tugas = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Task Status', default='draft')
    id_proyek = fields.Many2one('construction.project', string='Project')
    id_manajer_tugas = fields.Many2one('res.users', string='Task Manager', required=True)
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)

    # Add evaluation_ids One2many field
    evaluation_ids = fields.One2many('evaluation', 'id_tugas', string='Evaluations')
