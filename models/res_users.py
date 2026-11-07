from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # Relational
    # This domain gives the opportunity to mention the evaluated and non-evaluated domains
    property_ids = fields.One2many(
        "estate.property", "seller_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])]
    )