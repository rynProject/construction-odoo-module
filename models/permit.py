from odoo import models, fields, api
from datetime import datetime

class ConstructionPermit(models.Model):
    _name = 'construction.permit'
    _description = 'Construction Permit'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project', required=True)
    applicant_name = fields.Many2one('res.users', string='Applicant Name')
    permit_type = fields.Selection([
        ('building', 'Building Permit'),
        ('environmental', 'Environmental Permit'),
        # Add more types as needed
    ], string='Permit Type')
    permit_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Permit Status', default='pending')
    submission_date = fields.Date(string='Submission Date')
    approval_date = fields.Date(string='Approval Date')
    attachment = fields.Binary('Attachment', required=False)

    @api.model
    def _generate_evaluation_name(self):
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'PERMIT{today_date_str}')])
        return f'PERMIT{today_date_str}{evaluations_today + 1:04d}'

    @api.onchange('permit_status')
    def _onchange_permit_status(self):
        if self.permit_status == 'approved':
            self.approval_date = fields.Date.today()
            self.attachment = False  # Clear any existing attachment
            self._fields['attachment'].required = True
        else:
            self.approval_date = False
            self._fields['attachment'].required = False
True