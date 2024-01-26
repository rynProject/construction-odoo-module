from odoo import models, fields, api

class Material(models.Model):
    _name = 'construction.material'
    _description = 'Material'

    name = fields.Char(string='Material Name', required=True)
    available_stock = fields.Integer(string='Available Stock', readonly=True)
    average_price = fields.Float(string='Average Price', compute='_compute_average_price', store=True)
    purchase_ids = fields.One2many('construction.purchase', 'material_id', string='Purchases')
    budget_line_ids = fields.One2many('construction.budget.material.line', 'material_id', string='Budget Lines')

    @api.depends('purchase_ids.price', 'purchase_ids.quantity')
    def _compute_average_price(self):
        for material in self:
            total_amount = sum(purchase.price * purchase.quantity for purchase in material.purchase_ids)
            total_quantity = sum(purchase.quantity for purchase in material.purchase_ids)

            if total_quantity != 0:
                material.average_price = total_amount / total_quantity
            else:
                material.average_price = 0.0