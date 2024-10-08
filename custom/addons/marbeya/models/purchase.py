from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    length = fields.Float(string="Length (cm)", required=True)
    width = fields.Float(string="Width (cm)", required=True)
    area_sqm = fields.Float(string="Area (sqm)", compute='_compute_area', store=True)
    total_area = fields.Float(string="Total Area (sqm)", compute='_compute_total_area', store=True)


    @api.depends('length', 'width')
    def _compute_area(self):
        for line in self:
            if line.length and line.width:
                # Convert area from cm² to m² (1 sqm = 10,000 cm²)
                line.area_sqm = (line.length * line.width) / 10000
            else:
                line.area_sqm = 0


    @api.depends('area_sqm', 'product_qty')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.area_sqm * line.product_qty


    @api.depends('total_area', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        """
        Override default amount computation to use total_area instead of product_qty.
        """
        for line in self:
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.total_area, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total')
    def _compute_amount(self):
        """
        Override the amount computation to base it on the new logic
        of total_area in purchase.order.line
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal  # Sum of the new line totals (based on total_area)
                amount_tax += line.price_tax  # Sum of the line taxes
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })
