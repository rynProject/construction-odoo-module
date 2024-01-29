from odoo import models, fields, api
from datetime import datetime

class EquipmentMaintenance(models.Model):
    _name = 'construction.maintenance'
    _description = 'Equipment Maintenance'

    name = fields.Char(string='Ref', compute='_compute_name', store=True)
    equipment_id = fields.Many2one('construction.equipment', string='Equipment', required=True)
    maintenance_description = fields.Text(string='Maintenance Description')
    maintenance_date = fields.Date(string='Maintenance Date')
    maintenance_cost = fields.Float(string='Maintenance Cost')
    attachment = fields.Binary(string='Attachmnet', attachment=True)

    @api.depends('maintenance_date')
    def _compute_name(self):
        for maintenance in self:
            if maintenance.maintenance_date:
                date_str = maintenance.maintenance_date.strftime("%Y%m%d")
                existing_names = maintenance.search([('name', 'like', f'MNT{date_str}%')])

                if existing_names:
                    latest_name = max(existing_names.mapped('name'))
                    sequence_number = int(latest_name[len('MNT') + len(date_str):]) + 1
                else:
                    sequence_number = 1

                maintenance.name = f'MNT{date_str}{sequence_number:04d}'
            else:
                maintenance.name = False
