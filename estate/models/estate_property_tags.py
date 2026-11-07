from random import randint

from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index', default=lambda self: randint(1, 11))

    # ---------------------------------------- Constraints ----------------------------------------

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique.',
    )