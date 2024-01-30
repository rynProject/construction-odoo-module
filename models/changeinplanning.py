from odoo import models, fields, api
from datetime import datetime

class ChangeInPlanning(models.Model):
    _name = 'construction.changeinplanning'
    _description = 'Change in Planning'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name')
    project_id = fields.Many2one('construction.project', string='Project ID', required=True)
    change_description = fields.Text(string='Change Description')
    change_date = fields.Date(string='Change Date')
    cost_impact = fields.Integer(string='Cost Impact')

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'CHPLAN{today_date_str}')])
        return f'CHPLAN{today_date_str}{evaluations_today + 1:04d}'