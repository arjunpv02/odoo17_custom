
from odoo import fields,models,api
from datetime import timedelta,datetime
from odoo.exceptions import ValidationError,UserError

class TestModel5(models.Model):
    _name = "property.offer"
    _order = "price desc"
    
    price = fields.Float("Price")
    status = fields.Selection(
        [
            ('accepted','accepted'),
            ('refused','refused'),
            ('pending','pending'),
            ('new','new'),
        ],
        copy = False,
        string = "Status"
    )
    partner_id = fields.Many2one('res.partner',required=True,string = "Seller")
    property_id = fields.Many2one('estate_property',required=True,string = "Property")
    
    validity = fields.Integer(default = 7,string="Validity",store=True)
    expiery_date = fields.Date(compute="_compute_expiery_date",inverse="_inverse_validity",store=True)
    
    # concept of related field
    # here we are conncting the property type in the creation of offer
    # Realated field also similar to  the main
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The Offer price should be positiveeee')
    ]
    
    
        # Method to accept an offer
    def action_accept_offer(self):
        for offer in self:
            # Ensure only one offer is accepted for a property
            existing_accepted = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id)
            if existing_accepted:
                raise ValidationError("Only one offer can be accepted for a property.")

            # Update the offer status to accepted
            offer.status = 'accepted'
            
            # Update property details based on the accepted offer
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'seller_id': offer.property_id.seller_id.id,  # Assuming the salesperson is linked to the property model
                'selling_price': offer.price,
                'state': 'offer_accepted',  # Change the state of the property to indicate offer is accepted
            })
        return True
    
    @api.constrains('status', 'price')
    def _check_selling_price_90_float(self):
        for record in self:
            # Only check when the offer status is 'accepted'
            if record.status == 'accepted':
                # Check if selling price is less than 90% of expected price
                if record.property_id.selling_price and float_compare(record.property_id.selling_price, (record.expected_price * 0.9), precision_digits=2) < 0:
                    raise ValidationError("Selling price can't be less than 90% of expected Price")
  

    
    
    
# # editing part to compute related field
#     def action_accept_offer(self):
#         # when function is called status is updating
#         for record in self:
#             record.status = "accepted"           
#         # also make changes in buyer and selling price
#             record.property_id.buyer_id = record.partner_id
#             record.property_id.selling_price = record.price   # updating the related model
#             record.property_id.state = 'offer_accepted'
            
#         return True
    
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


    # to perform checkings and changing before inserting a record chapter 11 inheritance
    @api.model
    def create(self,vals):
        # we can get the inserting field to the model in this way
        # values of inserting module(property.offer)
        property_id = vals.get('property_id') 
        price = vals.get('price')
        print(price)
        print(property_id)
        # [imp] getting another connected record of another related model
        # getting related estate_property record
        property_record = self.env['estate_property'].browse(vals['property_id'])   # to get the whole record
        
        # problem 1: setting state = offer recieved when a module is created.
        property_record.state = 'offer_recieved'
        
        # problem 2: checking the new offer record have less price than existing record 
        existing_prices = property_record.offer_ids.mapped('price') 
        if existing_prices and price>max(existing_prices):
            raise UserError("Offer Price Shold be less than prev offers")
        
        return super().create(vals)

        
            

