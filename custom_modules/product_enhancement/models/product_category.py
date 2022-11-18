from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ProductCategoryEnhancement(models.Model):
    _inherit = 'product.category'

    code = fields.Char()

    @api.model
    def create(self, values):
        if'code' in values:
            code = self.env['product.category'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The Category code already exists.'))
        return super(ProductCategoryEnhancement, self).create(values)

    def write(self, values):
        if 'code' in values:
            code = self.env['product.category'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The Category code already exists.'))
        return super(ProductCategoryEnhancement, self).write(values)
