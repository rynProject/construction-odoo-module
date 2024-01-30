from datetime import datetime
from venv import logger
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Budget(models.Model):
    _name = 'construction.budget'
    _description = 'Budget Management'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
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
    worker_line_ids = fields.One2many('construction.budget.worker.line', 'budget_id', string='Worker Lines')
    equipment_line_ids = fields.One2many('construction.budget.equipment.line', 'budget_id', string='Equipment Lines')

    @api.depends('material_line_ids.total_amount', 'worker_line_ids.total_salary', 'equipment_line_ids.total_rent')
    def _compute_jumlah_anggaran(self):
        for rec in self:
            material_total = sum(rec.material_line_ids.mapped('total_amount'))
            worker_total = sum(rec.worker_line_ids.mapped('total_salary'))
            equipment_total = sum(rec.equipment_line_ids.mapped('total_rent'))
            total = material_total + worker_total + equipment_total
            rec.jumlah_anggaran = total
    
    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'BUD{today_date_str}')])
        return f'BUD{today_date_str}{evaluations_today + 1:04d}'

    @api.onchange('kategori_anggaran')
    def _onchange_kategori_anggaran(self):
        # If kategori_anggaran is not 'materials', delete material_line_ids and make it invisible
        if self.kategori_anggaran != 'materials':
            # Delete existing material records
            self.material_line_ids.unlink()

        # If kategori_anggaran is not 'worker', delete worker_line_ids and make it invisible
        if self.kategori_anggaran != 'worker':
            # Delete existing worker records
            self.worker_line_ids.unlink()

        # If kategori_anggaran is not 'equipment', delete equipment_line_ids and make it invisible
        if self.kategori_anggaran != 'equipment':
            # Delete existing equipment records
            self.equipment_line_ids.unlink()

    @api.model
    def create(self, values):
        # Call the original create method
        budget = super(Budget, self).create(values)

        # Additional logic for budget creation if needed

        return budget


class BudgetMaterialLine(models.Model):
    _name = 'construction.budget.material.line'
    _description = 'Budget Material Lines'

    material_id = fields.Many2one('construction.material', string='Material', required=True)
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

    def unlink(self):
        # Add the total quantity back to the associated material when deleting a BudgetMaterialLine
        for line in self:
            material = line.material_id
            material.write({
                'available_stock': material.available_stock + line.quantity
            })
            self.env.cr.commit()  # Commit the transaction immediately
            logger.info(f"Unlinking BudgetMaterialLine {line.id}")
        return super(BudgetMaterialLine, self).unlink()


class BudgetWorkerLine(models.Model):
    _name = 'construction.budget.worker.line'
    _description = 'Budget Worker Lines'

    worker_id = fields.Many2one('construction.worker', string='Worker', required=True)
    days_worked = fields.Float(string='Days Worked')
    salary = fields.Float(related='worker_id.salary', string='Salary')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary')
    budget_id = fields.Many2one('construction.budget', string='Budget')

    @api.depends('days_worked', 'salary')
    def _compute_total_salary(self):
        for line in self:
            line.total_salary = line.days_worked * line.salary

    def unlink(self):
        # Add the total days worked back to the associated worker when deleting a BudgetWorkerLine
        for line in self:
            worker = line.worker_id
            worker.write({
                'total_days_worked': worker.total_days_worked + line.days_worked
            })
            self.env.cr.commit()  # Commit the transaction immediately
            logger.info(f"Unlinking BudgetWorkerLine {line.id}")
        return super(BudgetWorkerLine, self).unlink()


class BudgetEquipmentLine(models.Model):
    _name = 'construction.budget.equipment.line'
    _description = 'Budget Equipment Lines'

    equipment_id = fields.Many2one('construction.equipment', string='Equipment', required=True)
    days_rented = fields.Integer(string='Days Rented')
    rent_price = fields.Integer(related='equipment_id.rent_price', string='Rent Price')
    total_rent = fields.Integer(string='Total Rent', compute='_compute_total_rent')
    budget_id = fields.Many2one('construction.budget', string='Budget')

    @api.depends('days_rented', 'rent_price')
    def _compute_total_rent(self):
        for line in self:
            line.total_rent = line.days_rented * line.rent_price

    def unlink(self):
        # Add the total days rented back to the associated equipment when deleting a BudgetEquipmentLine
        for line in self:
            equipment = line.equipment_id
            equipment.write({
                'total_days_rented': equipment.total_days_rented + line.days_rented
            })
            self.env.cr.commit()  # Commit the transaction immediately
            logger.info(f"Unlinking BudgetEquipmentLine {line.id}")
        return super(BudgetEquipmentLine, self).unlink()
