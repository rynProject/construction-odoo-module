from odoo import models, fields, api
from datetime import datetime

class ProgressNote(models.Model):
    _name = 'construction.progress'
    _description = 'Progress Note'

    ref = fields.Char('Ref', compute='_compute_ref', store=True)
    name = fields.Char(string='Name', required=True)
    id_proyek = fields.Many2one('construction.project', string='ID Proyek', required=True)
    catatan_kemajuan = fields.Text(string='Catatan Kemajuan')
    tanggal_pembuatan_catatan = fields.Date(string='Tanggal Pembuatan Catatan')
    create_uid = fields.Many2one('res.users', string='Created By', required=True)
    attachment = fields.Binary(string='Attachment', attachment=True, help='Attach a picture here.')

    @api.depends('name')
    def _compute_ref(self):
        for progress in self:
            if progress.name:
                current_date = datetime.now().strftime("%Y%m%d")
                ref_prefix = 'PROG'
                existing_refs = progress.search([('ref', 'like', f'{ref_prefix}{current_date}%')])

                if existing_refs:
                    latest_ref = max(existing_refs.mapped('ref'))
                    sequence_number = int(latest_ref[len(ref_prefix) + len(current_date):]) + 1
                else:
                    sequence_number = 1

                progress.ref = f'{ref_prefix}{current_date}{sequence_number:03d}'
