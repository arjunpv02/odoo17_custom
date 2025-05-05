from odoo import models,fields,api

class TestModel(models.Model):
    _name = "property_type"
    _description = "available property types in estate module"

    type_code = fields.Selection([
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('castle', 'Castle'),
        ('penthouse', 'Penthouse'),
    ], string="Type Code", required=True)

    name = fields.Char(string="Name", required=True)
    
    # creating one to many referencing to properties
    #  there is a corresponding many to one (property_type_id)
    property_ids = fields.One2many('estate_property','property_type_id',string="Prop ids")
    
    
    
