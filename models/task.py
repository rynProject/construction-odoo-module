from datetime import datetime
from odoo import api, models, fields

class Task(models.Model):
    _name = 'construction.task'
    _description = 'Project Task'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ref = fields.Char(string='Ref', required=True, copy=False, readonly=True, index=True, default=lambda self: self._generate_evaluation_name())
    name = fields.Char(string='Task', required=True)
    deskripsi_tugas = fields.Text(string='Description')
    tanggal_mulai = fields.Date(string='Start Date')
    tanggal_selesai = fields.Date(string='End Date')
    status_tugas = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancel', 'Canceled'),
    ], string='Task Status', default='draft')
    id_proyek = fields.Many2one('construction.project', string='Project')
    id_manajer_tugas = fields.Many2one('res.users', string='Task Manager', required=True)
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)

    # Add evaluation_ids One2many field
    evaluation_ids = fields.One2many('evaluation', 'id_tugas', string='Evaluations')

    def action_confirm(self):
        self.write({'status_tugas':'completed'})
    def action_done(self):
        self.write({'status_tugas':'completed'})
    def action_ongoing(self):
        self.write({'status_tugas':'ongoing'})
    def action_cancel(self):
        self.write({'status_tugas':'cancel'})
    def action_draft(self):
        self.write({'status_tugas':'draft'})

    @api.model
    def _generate_evaluation_name(self):
        # Generate a unique name in the format "BUF+date+auto increment"
        today_date_str = datetime.now().strftime('%Y%m%d')
        evaluations_today = self.search_count([('ref', 'like', f'TASK{today_date_str}')])
        return f'TASK{today_date_str}{evaluations_today + 1:04d}'