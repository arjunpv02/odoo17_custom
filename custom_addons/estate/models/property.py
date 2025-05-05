from odoo import models,fields,api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare,float_is_zero

class TestModel(models.Model):
    _name = "estate_property"
    _description = "real estate properties"
    _rec_name = "title"
    

    title = fields.Char("Title",required = True,index = True)
    
    
    property_type = fields.Selection(
        [
            ('house','house'),
            ('apartment','apartment'),
            ('castle','castle'),
            ('penthouse','pent_house'),
        ],string = "Property Type",required = True)
    
    # many to many relationship
    property_tags_ids = fields.Many2many('property.tags',string="Property Tags")
    
    # many to one relationship
    property_type_id = fields.Many2one('property_type',string = "property Type")
    
    # one to many
    offer_ids = fields.One2many("property.offer","property_id",string = "Offers")
    
    active = fields.Boolean()
    
    # code editing to button and action
    state = fields.Selection(
        [
            ('new','New'),
            ('offer_recieved','Offer Recieved'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],default = 'new'
    )
    
    post_code = fields.Integer("Post Code",required = True)
    tags = fields.Text("Tags")
    bedrooms = fields.Integer("Bed rooms")
    living_area = fields.Integer("Living Area(Sqm)")
    facades = fields.Integer()
    date_availabilty = fields.Date(copy = False)
    garden = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
    [
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ],
    string='Garden Orientation'
    )
    expected_price = fields.Float("Expected Price",digits = (12,2))
    selling_price = fields.Monetary("Selling Price",default = 0,currency_field ="currency_id",readonly='True',copy = False)
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    
    # advanced constraint using python 
    """@api.constrains('selling_price')       #decorate a constraint checker, checks every time any changes in selling price 
    def _check_selling_price_90(self):
        for record in self:
            
            # normaly checking logic if s_price not 0 and if (accepted not in status of records)
            if record.selling_price != 0 and "accepted" not in record.offer_ids.mapped("status"):
                #  throuwing exception
                raise ValidationError("Can't set a Selling Price when offer is not accepted")
                        
            if record.selling_price < (record.expected_price * .9 ):
                raise ValidationError("Selling price cant be less than 90 %  of expected Price")"""
            
    # same constrains using float methods, always use float methods 
    @api.constrains("selling_price")
    def _check_selling_prrice_90_float(self):
        for record in self:
            # getting a list of all the offer status in the record
            # mapped is used to get the status of the offer ids in the record
            offer_statuses = record.offer_ids.mapped("status")
            
            # [LOGIC]  if there is no status is accepted and if selling_price is not zero --> Throws exception
            if  not any (sts == "accepted" for sts in offer_statuses) and not float_is_zero(record.selling_price,precision_digits=2):
                raise ValidationError("Can't set a Selling Price when offer is not accepted")
            
            # [LOGIC] 
            if float_compare(record.selling_price,(record.expected_price * .9 ),precision_digits = 2) < 0:
                raise ValidationError("Selling price cant be less than 90 %  of expected Price")
                
    

    # creating 2 many to one fields
    
    # res.partner: a partner is a physical or legal entity. It can be a company, an individual or even a contact address.
    # res.users: the users of the system. Users can be ‘internal’, i.e. they have access to the Odoo backend. Or they can be ‘portal’, i.e. 
    # they cannot access the backend, only the frontend (e.g. to access their previous orders in eCommerce).
    
    # check the way of how we get connected to the res.partner and res.users models.
    # here we are creating a many2one field which is used to create a many to one relationship between the estate_property and res.partner and res.users models.
    buyer_id = fields.Many2one('res.partner',string="Buyer",copy=False)
    seller_id = fields.Many2one('res.users',string="Seller",default=lambda self: self.env.user)
    
    # compute field
    
    total_area = fields.Float(compute="_compute_total_area")
    
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'),default=0.0)
    
    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.garden_area + line.living_area
            
            
    @api.onchange("garden")
    def onchange_default_garden(self):
        if self.garden :
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False
            
#  button actions
   
    def action_set_sold(self):
        for record in self:
            self.state = "sold"
        return True
    
    
    def action_set_cancel(self):
        for record in self:
            self.state = "cancelled"
        return True
    
    
    #  SQL constraints to check wheather the price is positive

    _sql_constraints = [
    ('check_expected_price_1', 'CHECK (expected_price > 1)', 'Expected price must be greater than 1'), 
    ('unique_title_property_type', 'UNIQUE(title, property_type)', 'Title and Property Type must be unique'),
]

    
    # @api.constraints('selling_price','expected_price','best_price')
    # def _check_price(self):
    #     for record in self:
    #         if ((record.selling_price<0) or (record.expected_price<0) or (record.best_price<0)):
    #             raise ValidationError("Only Positive Values For Price")
            



class TestModel4(models.Model):
    _name = "property.tags"
    
    name = fields.Char(required = True, string = "Property tag")
    

# there is a model.Model class in odoo which is used to create a new model.
# The model.Model class is the base
#  Also there is other 2 models which are used to create a new model.

# Here we are creating a new model called property_type which is used to create a new model.
# we can also use TestModel1 and TestModel2 to create a new model as it is base class.
class TestModel1(models.Model):
    _name = "property_type"
    _description = "available property types in estate module"

    name = fields.Char(string ="proerty types", required=True)


class TestModel2(models.Model):
    _name = "test.property"
    
    title = fields.Char("Title",required = True,index = True)
    property_type_id = fields.Many2one('test.property.type',string="Property Type",required = True)
    
    
    
    
class TestModel3(models.Model):
    _name = "test.property.type"
    
    name = fields.Selection(
        [('house','house'),
         ('apartment','apartment'),
         ('castle','castle'),
         ('penthouse','pent_house'),],
        string = "property type",
        required = True,
        duplicate = False,
    )
    
    