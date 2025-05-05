
from odoo import fields,models,api
from datetime import timedelta,datetime
from odoo.exceptions import ValidationError

class TestModel5(models.Model):
    _name = "property.offer"
    
    price = fields.Float(string = "Price")
    status = fields.Selection(
        [
            ('accepted','accepted'),
            ('refused','refused'),
            ('pending','pending'),
        ],
        copy = False,
        string = "Status"
    )
    partner_id = fields.Many2one('res.partner',required=True,string = "Seller")
    property_id = fields.Many2one('estate_property',required=True,string = "Property")
    
    validity = fields.Integer(default = 7,string="Validity",store=True)
    expiery_date = fields.Date(compute="_compute_expiery_date",inverse="_inverse_validity",store=True)
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The Offer price should be positiveeee')
    ]
    
# editing part to compute related field
    def action_accept_offer(self):
        # when function is called status is updating
        for record in self:
            record.status = "accepted"           
        # also make changes in buyer and selling price
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price   # updating the related model
            
        return True
    
    @api.depends('status')
    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True   # public methord will always return something
    
    
    @api.depends('validity')  
    def _compute_expiery_date(self):    # compute methord is a private methord
        for record in self:
            if record.create_date:
                record.expiery_date = record.create_date + timedelta(days = record.validity)
            else:
                record.expiery_date =  datetime.now() + timedelta(days=record.validity)
                

    def _inverse_validity(self):
        for record in self:
            if record.create_date and record.expiery_date:
                create_date = record.create_date.date()     # converting datetime into date to avoind calculation error.
                if create_date > record.expiery_date:
                    raise ValidationError(" Expery must be after created at")   # not allowing saving a false value 
                record.validity = (record.expiery_date - create_date).days      # diff in days



