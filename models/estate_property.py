
from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user, required=True)
    description = fields.Text(string='Description')
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )   
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', default=lambda self: self._default_date_availability(), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    living_area = fields.Integer(string='Area (sq. m)')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sq. m)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string='Total Area (sq. m)', compute='_compute_total_area')
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    def _default_date_availability(self):
            return fields.Date.context_today(self) + relativedelta(months=3)


# Computed fields
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0
