from odoo import models, fields, api
from datetime import datetime

class ChangeInPlanning(models.Model):
    _name = 'construction.changeinplanning'
    _description = 'Change in Planning'

    ref = fields.Char(string='Ref', compute='_compute_name', store=True)
    name = fields.Char(string='Change ID')
    project_id = fields.Many2one('construction.project', string='Project ID', required=True)
    change_description = fields.Text(string='Change Description')
    change_date = fields.Date(string='Change Date')
    cost_impact = fields.Integer(string='Cost Impact')

    @api.depends('change_date')
    def _compute_name(self):
        for change in self:
            if change.change_date:
                date_str = change.change_date.strftime('%Y%m%d')
                changes_today = self.search_count([('name', 'like', f'CHPLAN{date_str}')])
                change.name = f'CHPLAN{date_str}{changes_today + 1:04d}'
            else:
                change.name = False
