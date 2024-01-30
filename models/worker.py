from datetime import datetime
from odoo import api, models, fields

class Worker(models.Model):
    _name = 'construction.worker'
    _description = 'Construction Worker'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name', required=True)
    position = fields.Selection([
        ('foreman', 'Foreman'),
        ('carpenter', 'Carpenter'),
        ('mason', 'Mason'),
        ('electrician', 'Electrician'),
        # Add more positions as needed
    ], string='Position')
    salary = fields.Float(string='Salary')

    # project_ids = fields.Many2many('construction.project', string='Assigned Projects', help='Projects where the worker is assigned')

    # You can add more fields as per your requirements
    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "BUF+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('ref', 'like', f'WORKER{today_date_str}')])
        return f'WORKER{today_date_str}{evaluations_today + 1:04d}'