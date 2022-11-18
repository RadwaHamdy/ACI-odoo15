import datetime
from odoo import models, fields, api, exceptions


class LotInherit(models.Model):
    _inherit = 'stock.production.lot'

    aci_production_date = fields.Date(required=True)
    product_ref = fields.Char(string='reference', related="product_id.default_code", store=True, readonly=False)

    # function for generation lot and updating expiration dates
    @api.onchange('product_id', 'aci_production_date')
    def _onchange_generate_lot(self):
        if self.aci_production_date:
            for rec in self:
                if not rec.product_id:
                    raise exceptions.UserError("Must Enter Product First")
                else:
                    if not rec.product_ref:
                        raise exceptions.UserError("This Product doesn't have a code or reference")
                    else:
                        ww = self.aci_production_date.strftime("%d%m%Y")
                        rec.name = str(rec.product_ref) + ww
                        # changing date
                        # expir_date = self.env['res.config.settings'].sudo().search([])
                        # if expir_date.module_product_expiry:
                        # updating dates
                        rec.expiration_date = rec.aci_production_date + datetime.timedelta(
                            days=rec.product_id.expiration_time)
                        rec.removal_date = rec.aci_production_date + datetime.timedelta(
                            days=rec.product_id.removal_time)
                        rec.use_date = rec.aci_production_date + datetime.timedelta(
                            days=rec.product_id.use_time)
                        rec.alert_date = rec.aci_production_date + datetime.timedelta(
                            days=rec.product_id.alert_time)

    # def _get_dates(self, product_id=None):
    #     """Returns dates based on number of days configured in current lot's product."""
    #     mapped_fields = {
    #         'expiration_date': 'expiration_time',
    #         'use_date': 'use_time',
    #         'removal_date': 'removal_time',
    #         'alert_date': 'alert_time'
    #     }
    #     res = dict.fromkeys(mapped_fields, False)
    #     product = self.env['product.product'].browse(product_id) or self.product_id
    #     if product:
    #         for field in mapped_fields:
    #             duration = getattr(product, mapped_fields[field])
    #             if duration:
    #                 dateexp = self.aci_production_date + datetime.timedelta(days=duration)
    #                 res[field] = fields.Datetime.to_string(dateexp)
    #     return res
