from odoo import models, fields, api
from datetime import datetime

class ConstructionPermit(models.Model):
    _name = 'construction.permit'
    _description = 'Construction Permit'

    name = fields.Char(string='ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: self._generate_permit_name())
    project_id = fields.Many2one('construction.project', string='Project', required=True)
    applicant_name = fields.Many2one('res.users',string='Applicant Name')
    permit_type = fields.Selection([
        ('building', 'Building Permit'),
        ('environmental', 'Environmental Permit'),
        # Add more types as needed
    ], string='Permit Type')
    permit_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Permit Status', default='pending', readonly=True)
    submission_date = fields.Date(string='Submission Date')
    approval_date = fields.Date(string='Approval Date')

    @api.model
    def _generate_permit_name(self):
        today = datetime.now().strftime('%Y%m%d')
        sequence_number = self.env['ir.sequence'].next_by_code('construction.permit') or '0001'
        return f'PERMIT{today}{sequence_number.zfill(4)}'
