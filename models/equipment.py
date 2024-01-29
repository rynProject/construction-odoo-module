from odoo import models, fields

class Equipment(models.Model):
    _name = 'construction.equipment'
    _description = 'Construction Equipment'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    availability = fields.Boolean(string='Availability', default=True)
    total_unit = fields.Integer(string='Total Unit')
    rent_price = fields.Integer(string='Rent Price')
    vendor = fields.Many2one('res.partner', string='Vendor')
    maintenance_ids = fields.One2many('construction.maintenance', 'equipment_id', string='Maintenance Records')