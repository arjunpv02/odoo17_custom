from odoo import models,fields,api


class TestModel(models.Model):
    _name = "estate.property.tags"
    _description = "different types(features) of estate properties."
    
    name = fields.Char(required=True,string="Property Tag")
    color = fields.Integer(default = 1)