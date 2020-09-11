from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError

class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    def _compute_paid_invoices(self):
        for rec in self:
            res = ""
            invs = []
            for inv in rec.matched_move_line_ids:
                if inv.move_id.name not in invs:
                    invs.append(inv.move_id.name)
            res = ",".join(invs)
            rec.paid_invoices = res

    def _search_paid_invoices(self, operator, value):
        if operator in ['ilike','='] and value:
            return_list = []
            payment_groups = self.env['account.payment.group'].search([])
            for payment_group in payment_groups:
                for inv in payment_group.matched_move_line_ids:
                    if value in inv.move_id.name:
                        return_list.append(payment_group.id)
            return [('id', 'in', return_list)]
        else:
            return [('id', 'in', [])]

    paid_invoices = fields.Char('Facturas pagadas',compute=_compute_paid_invoices,search=_search_paid_invoices)

