from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Gestion des propriétés immobilières'
    
    name = fields.Char(string="Nom de la propriété", required=True)
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Prix attendu", required=True)
    selling_price = fields.Float(string="Prix de vente", readonly=True)
    state = fields.Selection(
        [('new', 'Nouveau'), ('offer_received', 'Offre reçue'), ('sold', 'Vendu')],
        string="Statut", default='new'
    )

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Le prix attendu doit être positif !')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < 0:
                raise ValidationError("Le prix de vente doit être positif !")

    def action_sell(self):
        self.write({'state': 'sold'})

    def action_cancel(self):
        self.write({'state': 'new'})
