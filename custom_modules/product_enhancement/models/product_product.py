from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ProductProductEnhancement(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product Enhancement'

    def default_get(self, default_fields):
        res = super(ProductProductEnhancement, self).default_get(default_fields)
        res['name'] = 'New'
        return res

    product_type = fields.Selection(string="Code Type",
                                    selection=[
                                        ('finished_product', 'Finished product'),
                                        ('packaging_material', 'Packaging material'),
                                    ],
                                    required=False, )
    packaging_type = fields.Selection(string="packaging Type",
                                      selection=[
                                          ('foreign', 'Foreign'),
                                          ('local', 'Local'),
                                      ],
                                      required=False, )

    brand_id = fields.Many2one(comodel_name='brand.name')
    product_type_id = fields.Many2one(comodel_name='product.type')
    product_version_id = fields.Many2one(comodel_name='product.version')
    product_subtype_id = fields.Many2one(comodel_name='product.subtype')

    @api.onchange('product_type_id')
    def onchange_type_id(self):
        if self.product_type_id:
            subtype_ids = self.product_type_id.subtype_ids.ids
            return {'domain': {'product_subtype_id': [('id', 'in', subtype_ids)]}}
        else:
            return {'domain': {'product_subtype_id': []}}

    def _product_sku_validation(self, vals):
        """
        This function checks the values and the existence of the codes.
        :param: vals: product values
        :return: first: first code part,
                second: second code part,
                 third: third code part,
                 product_name
        :raise: validationError if messing date .
        """
        code = product_name = False
        if 'product_type' not in vals or not vals.get('product_type', False):
            raise ValidationError(_('You must Select ( Finished product / Packaging material).'))
        product_type = vals.get('product_type', False)
        if not vals.get('uom_id', False) or 'uom_id' not in vals:
            raise ValidationError(_('There is No Unit of Measure.'))
        if not vals.get('categ_id', False) or 'categ_id' not in vals:
            raise ValidationError(_('There is No Product Category.'))
        if not vals.get('brand_id', False) or 'brand_id' not in vals:
            raise ValidationError(_('There is No Brand Name.'))

        uom = self.env['uom.uom'].browse(vals['uom_id'])
        categ = self.env['product.category'].browse(vals['categ_id'])
        brand = self.env['brand.name'].browse(vals['brand_id'])

        if not uom.code:
            raise ValidationError(_('There is No Unit of Measure code.'))
        if not categ.code:
            raise ValidationError(_('There is No Product Category code.'))
        if not brand.code:
            raise ValidationError(_('There is No Brand Name code.'))

        if product_type == 'finished_product':
            product_name = "%s %s %s" % (brand.name, categ.name, uom.name)
            code = "%s%s%s" % (brand.code, categ.code, uom.code)
            return code, product_name
        elif product_type == 'packaging_material':
            if not vals.get('product_version_id', False) or 'product_version_id' not in vals:
                raise ValidationError(_('There is No Product Version.'))
            if not vals.get('product_type_id', False) or 'product_type_id' not in vals:
                raise ValidationError(_('There is No Type.'))
            if not vals.get('product_subtype_id', False) or 'product_subtype_id' not in vals:
                raise ValidationError(_('There is No SubType.'))

            version = self.env['product.version'].browse(vals['product_version_id'])
            ptype = self.env['product.type'].browse(vals['product_type_id'])
            subtype = self.env['product.subtype'].browse(vals['product_subtype_id'])

            if not version.code:
                raise ValidationError(_('There is No Product Version code.'))
            if not ptype.code:
                raise ValidationError(_('There is No Type code.'))
            if not subtype.code:
                raise ValidationError(_('There is No Product SubType code.'))

            product_name = "%s %s %s %s %s %s" % (
                ptype.name, subtype.name, brand.name, categ.name, uom.name, version.name)
            code = "%s%s%s%s%s%s" % (ptype.code, subtype.code, brand.code, categ.code, uom.code, version.code)
            return code, product_name

    def _check_code_exists(self, code):
        if self.id:
            code_count = self.env['product.product'].search_count(
                [('default_code', '=', code), ('id', '!=', self.id), ('active', 'in', False or True)])
        else:
            code_count = self.env['product.product'].search_count(
                [('default_code', '=', code),('active', 'in', False or True)])
        if code_count > 0:
            raise ValidationError(_('The Product code already exists.'))
        return True

    @api.model
    def create(self, values):
        print('.....',values)
        if values:
            code, product_name = self._product_sku_validation(values)
            if self._check_code_exists(code) and product_name:
                values['default_code'] = code
                values['name'] = product_name
        return super(ProductProductEnhancement, self).create(values)

    def write(self, values):
        fields = [
            'product_type', 'uom_id', 'categ_id',
            'brand_id', 'product_version_id', 'product_type_id',
            'product_subtype_id'
        ]
        update_product = []
        vals = {}
        for field in fields:
            if field == 'product_type':
                if field in values:
                    vals[field] = values.get('product_type', False)
                    update_product.append(True)
                else:
                    vals[field] = self.product_type
                    update_product.append(False)
            else:
                if field in values:
                    vals[field] = values.get(field, False)
                    update_product.append(True)
                else:
                    update_product.append(False)
                    vals[field] = self[field].id

        if any(update_product):
            code, product_name = self._product_sku_validation(vals)
            if self._check_code_exists(code) and product_name:
                values['default_code'] = code
                values['name'] = product_name
        return super(ProductProductEnhancement, self).write(values)


class ProductType(models.Model):
    _name = 'product.type'
    _description = 'Product Type'

    name = fields.Char(required=False, )
    code = fields.Char(required=False, )
    subtype_ids = fields.One2many("product.subtype", "type_id", string="SubTypes", required=False, )

    @api.model
    def create(self, values):
        if'code' in values:
            code = self.env['product.type'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The type code already exists.'))
        return super(ProductType, self).create(values)

    def write(self, values):
        if 'code' in values:
            code = self.env['product.type'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The type code already exists.'))
        return super(ProductType, self).write(values)


class ProductVersion(models.Model):
    _name = 'product.version'
    _description = 'Product Version'

    name = fields.Char(required=False, )
    code = fields.Char(required=False, )

    @api.model
    def create(self, values):
        if'code' in values:
            code = self.env['product.version'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The version code already exists.'))
        return super(ProductVersion, self).create(values)

    def write(self, values):
        if 'code' in values:
            code = self.env['product.version'].search_count([('code', '=', values['code'])])
            if code > 0:
                raise ValidationError(_('The version code already exists.'))
        return super(ProductVersion, self).write(values)


class ProductSubType(models.Model):
    _name = 'product.subtype'
    _description = 'Product SubType'

    name = fields.Char(required=True, )
    code = fields.Char(required=False, )
    type_id = fields.Many2one("product.type", string="Parent Type", required=True)

    @api.model
    def create(self, values):
        if 'type_id' in values and 'code' in values:
            code = self.env['product.subtype'].search_count(
                [('code', '=', values['code']), ('type_id', '=', values['type_id'] )])
            if code > 0:
                raise ValidationError(_('the Subtype code already exists.'))
        return super(ProductSubType, self).create(values)

    def write(self, values):
        if 'type_id' in values and 'code' in values:
            code = self.env['product.subtype'].search_count(
                [('code', '=', values['code']), ('type_id', '=', values['type_id'])])
            if code > 0:
                raise ValidationError(_('the Subtype code already exists.'))
        return super(ProductSubType, self).write(values)
