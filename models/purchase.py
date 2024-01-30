from odoo import models, fields, api
from datetime import datetime

class Purchase(models.Model):
    _name = 'construction.purchase'
    _description = 'Purchase'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Invoice Number', readonly=True, default=lambda self: self._get_next_invoice_number())
    material_id = fields.Many2one('construction.material', string='Material', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    price = fields.Integer(string='Price')
    total = fields.Integer(string='Total', readonly=True)
    purchase_date = fields.Date(string='Purchase Date', required=True, default=fields.Date.today())
    create_uid = fields.Many2one('res.users', string='Created By', required=True)

    attachment_ids = fields.Binary(string='Attachments')

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "BUF+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('ref', 'like', f'INV{today_date_str}')])
        return f'INV{today_date_str}{evaluations_today + 1:04d}'

    @api.model
    def _get_next_invoice_number(self):
        # Generate the next invoice number based on the current date and an auto-incrementing number
        today_str = datetime.now().strftime('%d%m%y')
        last_purchase = self.search([], limit=1, order='create_date desc')
        if last_purchase:
            last_number = int(last_purchase.name[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f'PRC{today_str}{new_number:04}'

    @api.model
    def create(self, values):
        # Calculate the total based on quantity and price
        values['total'] = values.get('quantity', 0) * values.get('price', 0)

        # Call the original create method
        purchase = super(Purchase, self).create(values)

        # Update the available_stock in the associated material
        material = purchase.material_id
        material.write({
            'available_stock': material.available_stock + purchase.quantity
        })

        return purchase
