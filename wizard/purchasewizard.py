from odoo import models, fields, api

class ReportPenjualanWz(models.TransientModel):
    _name = 'construction.purchasereportwz'
    _description = 'model.technical.name'

    dari_tgl = fields.Date(string='dari Tanggal', required=True)
    ke_tgl = fields.Date(string='ke Tanggal', required=True, default=fields.Date().today())
    # penjualan_id = fields.Many2one(comodel_name='consruction.purchase', string='')
    

    def action_purchase_report(self):
        laporan = []
        dari = self.dari_tgl
        ke = self.ke_tgl
        if dari:
            laporan += [('purchase_date','>=', dari)]
        if ke:
            laporan += [('purchase_date','<=', ke)]
        print(laporan)
        laporan_jadi = self.env['construction.purchase'].search_read(laporan)
        data = {
            'form' : self.read()[0],
            'laporannya' : laporan_jadi            
        }
        report_action = self.env.ref('construction.purchase_report_wizard').report_action(self, data=data)
        report_action['close_on_report_download'] = True
        return report_action