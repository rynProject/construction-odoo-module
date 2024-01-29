from odoo import models, fields, api
from datetime import datetime

class SecurityInspection(models.Model):
    _name = 'construction.security'
    _description = 'Security Inspection'

    project_id = fields.Many2one('construction.project', string='Project', required=True)
    inspection_notes = fields.Text(string='Security Inspection Notes')
    attachment = fields.Binary(string='Attachment', attachment=True)
    inspection_date = fields.Date(string='Inspection Date')
    preventive_action = fields.Text(string='Preventive Action')
    
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    @api.depends('inspection_date')
    def _compute_name(self):
        for security in self:
            if security.inspection_date:
                date_str = security.inspection_date.strftime("%Y%m%d")
                existing_names = security.search([('name', 'like', f'SECINS{date_str}%')])

                if existing_names:
                    latest_name = max(existing_names.mapped('name'))
                    sequence_number = int(latest_name[len('SECINS') + len(date_str):]) + 1
                else:
                    sequence_number = 1

                security.name = f'SECINS{date_str}{sequence_number:04d}'
            else:
                security.name = False
