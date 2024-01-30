import datetime
from odoo import api, models, fields

class Equipment(models.Model):
    _name = 'construction.equipment'
    _description = 'Construction Equipment'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    
    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    availability = fields.Boolean(string='Availability', default=True)
    total_unit = fields.Integer(string='Total Unit')
    rent_price = fields.Integer(string='Rent Price')
    vendor = fields.Many2one('res.partner', string='Vendor')
    maintenance_ids = fields.One2many('construction.maintenance', 'equipment_id', string='Maintenance Records')

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'EQUIP{today_date_str}')])
        return f'EQUIP{today_date_str}{evaluations_today + 1:04d}'