from odoo import models, fields, api
from datetime import datetime

class SecurityInspection(models.Model):
    _name = 'construction.security'
    _description = 'Security Inspection'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    project_id = fields.Many2one('construction.project', string='Project', required=True)
    inspection_notes = fields.Text(string='Security Inspection Notes')
    attachment = fields.Binary(string='Attachment', attachment=True)
    inspection_date = fields.Date(string='Inspection Date')
    preventive_action = fields.Text(string='Preventive Action')
    
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "BUF+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('ref', 'like', f'SECINS{today_date_str}')])
        return f'SECINS{today_date_str}{evaluations_today + 1:04d}'