from odoo import models,fields,api

class TestModel(models.Model):
    _name = "property_type"
    _description = "available property types in estate module"
    _order = "name"

    type_code = fields.Selection([
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('castle', 'Castle'),
        ('penthouse', 'Penthouse'),
    ], string="Type Code", required=True)

    name = fields.Char(string="Name", required=True)
    
    # creating one to many referencing to properties
    #  there is a corresponding many to one (property_type_id)
    property_ids = fields.One2many('estate_property','property_type_id',string="Properties")
    
    sequence = fields.Integer(string = "Sequence", default=1, help = "to order according to the property type")
    
    # related one2many to the field in property offer
    offer_ids = fields.One2many('property.offer','property_type_id',string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    
    # function to calculate the number of offers in this property type
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            count = 0
            for i in record.offer_ids:
                count += 1
            record.offer_count=count
            
    
    
    
