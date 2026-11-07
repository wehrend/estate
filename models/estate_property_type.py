

from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string='Name', required=True)

 # ---------------------------------------- Constraints -------------------------------------

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique.',
)

