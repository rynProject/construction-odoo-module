from odoo import models, fields, api

class Project(models.Model):
    _name = 'construction.project'
    _description = 'Project Management'

    name = fields.Char(string='Project Name', required=True)
    lokasi_proyek = fields.Char(string='Location')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_proyek = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Status Proyek', default='draft')
    id_manajer_proyek = fields.Many2one('res.users', string='Project Manager', required=True)

    task_ids = fields.One2many(comodel_name='construction.task', inverse_name='id_proyek', string='Task List')
    budget_ids = fields.One2many(comodel_name='construction.budget', inverse_name='id_proyek', string='Budget List')
    
    total_budget = fields.Integer(string='Total Budget', compute='_compute_total_budget', store=True)

    @api.depends('budget_ids.jumlah_anggaran')
    def _compute_total_budget(self):
        for project in self:
            project.total_budget = sum(budget.jumlah_anggaran for budget in project.budget_ids)
