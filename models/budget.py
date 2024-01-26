from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Budget(models.Model):
    _name = 'construction.budget'
    _description = 'Budget Management'

    name = fields.Char(string='Name')
    id_proyek = fields.Many2one('construction.project', string='Project', required=True)
    kategori_anggaran = fields.Selection([
        ('worker', 'Workers'),
        ('materials', 'Materials'),
        ('equipment', 'Equipment'),
    ], string='Category', default='draft')
    jumlah_anggaran = fields.Float(string='Amount', compute='_compute_jumlah_anggaran', store=True)
    tanggal_pembuatan_anggaran = fields.Date(string='Created Date', default=fields.Date.today())
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)

    material_line_ids = fields.One2many('construction.budget.material.line', 'budget_id', string='Material Lines')

    @api.depends('material_line_ids.total_amount')
    def _compute_jumlah_anggaran(self):
        for rec in self:
            total = sum(rec.material_line_ids.mapped('total_amount'))
            print("Total Harga = ", total)
            rec.jumlah_anggaran = total

class BudgetMaterialLine(models.Model):
    _name = 'construction.budget.material.line'
    _description = 'Budget Material Lines'

    material_id = fields.Many2one('construction.material', string='Material', required=True)

    @api.onchange('kategori_anggaran')
    def _onchange_kategori_anggaran(self):
        # Make material_line_ids visible when kategori_anggaran is 'materials'
        if self.kategori_anggaran == 'materials':
            # Remove existing records (if any)
            self.material_line_ids.unlink()

            # Add a new empty record
            self.material_line_ids.create({})

            # Set invisible attribute to False
            self.material_line_ids.invisible = False
        else:
            # Set invisible attribute to True
            self.material_line_ids.invisible = True



    quantity = fields.Integer(string='Quantity')
    average_price = fields.Float(related='material_id.average_price', string='average_price')
    total_amount = fields.Float(string='Total amount', compute='_compute_total_amount')
    budget_id = fields.Many2one('construction.budget', string='Budget')

    @api.depends('quantity', 'average_price')
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = line.quantity * line.average_price

    @api.model
    def create(self, values):
        # Validate material quantity before creating the budget material line
        line_quantity = values.get('quantity', 0)
        material = self.env['construction.material'].browse(values.get('material_id'))

        if material.available_stock < line_quantity:
            raise ValidationError('The material quantity is insufficient. Cannot create the budget material line.')

        # Call the original create method
        line = super(BudgetMaterialLine, self).create(values)

        # Decrease the quantity on the associated material
        material.write({
            'available_stock': material.available_stock - line.quantity
        })

        return line