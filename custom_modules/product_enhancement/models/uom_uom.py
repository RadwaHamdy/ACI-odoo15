from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class UoMEnhancement(models.Model):
    _inherit = 'uom.uom'

    code = fields.Char()

    @api.model
    def create(self, values):
        if 'code' in values:
            code = self.env['uom.uom'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The Unit of Measure code already exists.'))
        return super(UoMEnhancement, self).create(values)

    def write(self, values):
        if 'code' in values:
            code = self.env['uom.uom'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The Category code already exists.'))
        return super(UoMEnhancement, self).write(values)
