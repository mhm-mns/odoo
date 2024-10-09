from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    length = fields.Float(string="Length (cm)", required=True)
    width = fields.Float(string="Width (cm)", required=True)
    count_of_slabs = fields.Float(string="Count Of Slabs (NOS)", default=1)
    product_qty = fields.Float(string="Total Area (sqm)", compute='_compute_total_area', readonly=True, store=True)


    @api.depends('length', 'width', 'count_of_slabs')
    def _compute_total_area(self):
        for line in self:
            line.product_qty = (line.length * line.width) / 10000 * line.count_of_slabs