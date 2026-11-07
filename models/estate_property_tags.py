from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

# ---------------------------------------- Constraints -------------------------------------
    _unique_name = models.Constraint(
    'UNIQUE(name)',
    'The name must be unique.',
)