from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    material_type = fields.Char(string="Material Type")
    finish = fields.Char(string="Finish")
    thickness = fields.Float(string="Thickness (cm)")
    