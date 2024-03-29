from urllib.parse import urlencode
import webbrowser
from odoo import models, fields, api
from datetime import datetime

class Project(models.Model):
    _name = 'construction.project'
    _description = 'Project Management'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Project Name', required=True)
    client = fields.Many2one(comodel_name='res.partner', string='Client')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_proyek = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancel', 'Canceled'),
    ], string='Status Proyek', default='draft')
    id_manajer_proyek = fields.Many2one('res.users', string='Project Manager', required=True)

    task_ids = fields.One2many(comodel_name='construction.task', inverse_name='id_proyek', string='Task List')
    budget_ids = fields.One2many(comodel_name='construction.budget', inverse_name='id_proyek', string='Budget List')
    expenditure_ids = fields.One2many(comodel_name='construction.expenditure', inverse_name='id_proyek', string='Expenditures')
    progress_ids = fields.One2many(comodel_name='construction.progress', inverse_name='id_proyek')
    changeinplan_ids = fields.One2many(comodel_name='construction.changeinplanning', inverse_name='project_id', string='Change in Plans')
    security_ids = fields.One2many(comodel_name='construction.security', inverse_name='project_id', string='Security')
    permit_ids = fields.One2many(comodel_name='construction.permit', inverse_name='project_id', string='Permit')
    
    lokasi = fields.Char(string='Location')
    latitude = fields.Float(string='Latitude', digits=(8, 6))
    longitude = fields.Float(string='Longitude', digits=(9, 6))
    
    total_budget = fields.Integer(string='Total Budget', compute='_compute_total_budget', store=True)
    total_expenditure = fields.Integer(string='Total Expenditure', compute='_compute_total_expenditure', store=True)
    total_impact_cost = fields.Float(string='Total Impact Cost', compute='_compute_total_impact_cost', store=True)

    def action_confirm(self):
        self.write({'status_proyek':'completed'})
    def action_done(self):
        self.write({'status_proyek':'completed'})
    def action_ongoing(self):
        self.write({'status_proyek':'ongoing'})
    def action_cancel(self):
        self.write({'status_proyek':'cancel'})
    def action_draft(self):
        self.write({'status_proyek':'draft'})

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "BUF+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('ref', 'like', f'PROJECT{today_date_str}')])
        return f'PROJECT{today_date_str}{evaluations_today + 1:04d}'
    
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

    def open_whatsapp_with_location(self):
        base_url = "https://wa.me/?"
        location_data = {'text': f"Check out the project location: https://www.google.com/maps/place/{self.latitude},{self.longitude}"}
        whatsapp_url = base_url + urlencode(location_data)

        # Open the WhatsApp link in the default web browser
        webbrowser.open(whatsapp_url, new=2)
