from odoo import models, fields, api
from datetime import datetime

class ProgressNote(models.Model):
    _name = 'construction.progress'
    _description = 'Progress Note'

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Name', required=True)
    id_proyek = fields.Many2one('construction.project', string='ID Proyek', required=True)
    catatan_kemajuan = fields.Text(string='Catatan Kemajuan')
    tanggal_pembuatan_catatan = fields.Date(string='Tanggal Pembuatan Catatan')
    create_uid = fields.Many2one('res.users', string='Created By', required=True)
    attachment = fields.Binary(string='Attachment', attachment=True, help='Attach a picture here.')

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "EVAL+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('name', 'like', f'PROGR{today_date_str}')])
        return f'PROGR{today_date_str}{evaluations_today + 1:04d}'