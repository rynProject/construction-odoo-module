from urllib.parse import urlencode
import webbrowser
from odoo import models, fields, api
from datetime import datetime

class Project(models.Model):
    _name = 'construction.project'
    _description = 'Project Management'

    ref = fields.Char(string='Ref', compute='_compute_ref', store=True)
    name = fields.Char(string='Project Name', required=True)
    client = fields.Many2one(comodel_name='res.partner', string='Client')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_proyek = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Status Proyek', default='draft')
    id_manajer_proyek = fields.Many2one('res.users', string='Project Manager', required=True)

    project_count = fields.Integer(string='Project Count', compute='_compute_project_count', store=True)
    task_ids = fields.One2many(comodel_name='construction.task', inverse_name='id_proyek', string='Task List')
    budget_ids = fields.One2many(comodel_name='construction.budget', inverse_name='id_proyek', string='Budget List')
    expenditure_ids = fields.One2many(comodel_name='construction.expenditure', inverse_name='id_proyek', string='Expenditures')
    progress_ids = fields.One2many(comodel_name='construction.progress', inverse_name='id_proyek')
    changeinplan_ids = fields.One2many(comodel_name='construction.changeinplanning', inverse_name='project_id', string='Change in Plans')
    
    lokasi = fields.Char(string='Location')
    latitude = fields.Float(string='Latitude', digits=(8, 6))
    longitude = fields.Float(string='Longitude', digits=(9, 6))
    
    total_budget = fields.Integer(string='Total Budget', compute='_compute_total_budget', store=True)
    total_expenditure = fields.Integer(string='Total Expenditure', compute='_compute_total_expenditure', store=True)
    total_impact_cost = fields.Float(string='Total Impact Cost', compute='_compute_total_impact_cost', store=True)

    @api.depends('name')
    def _compute_ref(self):
        for project in self:
            if project.name:
                current_date = datetime.now().strftime("%Y%m%d")
                ref_prefix = 'PROJECT'
                existing_refs = project.search([('ref', 'like', f'{ref_prefix}{current_date}%')])

                if existing_refs:
                    latest_ref = max(existing_refs.mapped('ref'))
                    sequence_number = int(latest_ref[len(ref_prefix) + len(current_date):]) + 1
                else:
                    sequence_number = 1

                project.ref = f'{ref_prefix}{current_date}{sequence_number:04d}'
    
    @api.depends('budget_ids.jumlah_anggaran')
    def _compute_total_budget(self):
        for project in self:
            project.total_budget = sum(budget.jumlah_anggaran for budget in project.budget_ids)

    @api.depends('expenditure_ids.jumlah_pengeluaran')
    def _compute_total_expenditure(self):
        for project in self:
            project.total_expenditure = sum(expenditure.jumlah_pengeluaran for expenditure in project.expenditure_ids)
    
    @api.depends('changeinplan_ids.cost_impact')
    def _compute_total_impact_cost(self):
        for project in self:
            project.total_impact_cost = sum(change.cost_impact for change in project.changeinplan_ids)

    @api.depends('ref')
    def _compute_project_count(self):
        for project in self:
            project.project_count = self.search_count([])

    def open_whatsapp_with_location(self):
        base_url = "https://wa.me/?"
        location_data = {'text': f"Check out the project location: https://www.google.com/maps/place/{self.latitude},{self.longitude}"}
        whatsapp_url = base_url + urlencode(location_data)

        # Open the WhatsApp link in the default web browser
        webbrowser.open(whatsapp_url, new=2)
