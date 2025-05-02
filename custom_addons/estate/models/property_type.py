from odoo import models,fields

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