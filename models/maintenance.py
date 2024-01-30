from odoo import models, fields, api
from datetime import datetime

class EquipmentMaintenance(models.Model):
    _name = 'construction.maintenance'
    _description = 'Equipment Maintenance'
    
    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name')
    equipment_id = fields.Many2one('construction.equipment', string='Equipment', required=True)
    maintenance_description = fields.Text(string='Maintenance Description')
    maintenance_date = fields.Date(string='Maintenance Date')
    maintenance_cost = fields.Integer(string='Maintenance Cost')
    attachment = fields.Binary(string='Attachmnet', attachment=True)

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'MNT{today_date_str}')])
        return f'MNT{today_date_str}{evaluations_today + 1:04d}'