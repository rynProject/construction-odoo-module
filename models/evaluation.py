from odoo import models, fields, api
from datetime import datetime

class Evaluation(models.Model):
    _name = 'evaluation'
    _description = 'Evaluation Model'

    name = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    id_tugas = fields.Many2one('construction.task', string='Task', required=True)
    penilaian_kinerja = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ], string='Work Assesment', required=True)
    komentar_evaluasi = fields.Text(string='Evaluation Comment')
    tanggal_evaluasi = fields.Date(string='Evaluation Date')
    attachment = fields.Binary(string='Attachment', attachment=True, help='Attach a picture here.')

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'EVAL{today_date_str}')])
        return f'EVAL{today_date_str}{evaluations_today + 1:04d}'

    @api.model
    def create(self, values):
        # If the name is not provided, generate a unique name
        if not values.get('name'):
            values['name'] = self._generate_evaluation_name()
        return super(Evaluation, self).create(values)
