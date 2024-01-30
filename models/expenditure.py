import datetime
from odoo import api, models, fields

class Expenditure(models.Model):
    _name = 'construction.expenditure'
    _description = 'Expenditure Management'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name')
    id_proyek = fields.Many2one('construction.project', string='ID Proyek', required=True)
    deskripsi_pengeluaran = fields.Text(string='Deskripsi Pengeluaran')
    jumlah_pengeluaran = fields.Float(string='Jumlah Pengeluaran')
    tanggal_pengeluaran = fields.Date(string='Tanggal Pengeluaran')
    create_uid = fields.Many2one('res.users', string='Created By', required=True)

    attachment = fields.Binary(string='Attachment', attachment=True)

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'EXP{today_date_str}')])
        return f'EXP{today_date_str}{evaluations_today + 1:04d}'