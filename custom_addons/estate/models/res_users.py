from odoo import models,api,fields
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit='res.users'
    
    property_ids = fields.One2many(
        'estate_property',
        'seller_id',
        string = "properties",
        domain = [('state','in',['new','offer_recieved'])]
    )
    
