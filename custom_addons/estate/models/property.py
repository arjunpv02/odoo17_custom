from odoo import models,fields,api

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
    property_type_id = fields.Many2one('property_type',string = "property type m2o")
    
    # one to many
    offer_ids = fields.One2many("property.offer","property_id",string = "Offers")
    
    active = fields.Boolean()
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
    
    