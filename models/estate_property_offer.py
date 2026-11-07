from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price', required=True)
    state = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    

    # Computed
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

# ---------------------------------------- CRUD Methods -------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env["estate.property"].browse(vals["property_id"])
            if float_compare(vals["price"], prop.best_price, precision_rounding=0.01) <= 0:
                raise UserError(f"The offer must be higher than {prop.best_price:.2f}.")
            prop.state = "offer_received"
        return super().create(vals_list)

# ---------------------------------------- Action Methods -------------------------------------

    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer has already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )

# ---------------------------------------- Constraints -------------------------------------

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )