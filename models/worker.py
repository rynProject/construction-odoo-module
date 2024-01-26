from odoo import models, fields

class Worker(models.Model):
    _name = 'construction.worker'
    _description = 'Construction Worker'

    name = fields.Char(string='Name', required=True)
    position = fields.Selection([
        ('foreman', 'Foreman'),
        ('carpenter', 'Carpenter'),
        ('mason', 'Mason'),
        ('electrician', 'Electrician'),
        # Add more positions as needed
    ], string='Position')
    salary = fields.Float(string='Salary')

    # project_ids = fields.Many2many('construction.project', string='Assigned Projects', help='Projects where the worker is assigned')

    # You can add more fields as per your requirements
