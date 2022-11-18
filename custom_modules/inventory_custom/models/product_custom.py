from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError, UserError


class ProductInherit(models.Model):
    _inherit = 'product.template'

    brand_name = fields.Many2one(comodel_name='brand.name')
    is_canseal = fields.Boolean(string='Is Canseal Product')
    is_competitor = fields.Boolean(string='Is Competitor Product')
    is_gift_product = fields.Boolean(string='Is Gift Product')


class BrandName(models.Model):
    _name = "brand.name"

    name = fields.Char(string='name')
    code = fields.Char()

    @api.model
    def create(self, values):
        if'code' in values:
            code = self.env['brand.name'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError('The BrandName code already exists.')
        return super(BrandName, self).create(values)

    def write(self, values):
        if 'code' in values:
            code = self.env['brand.name'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError('The BrandName code already exists.')
        return super(BrandName, self).write(values)


