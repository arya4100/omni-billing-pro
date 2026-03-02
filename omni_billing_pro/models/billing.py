from odoo import api, fields, models, _
from odoo.exceptions import UserError

class OmniInvoice(models.Model):
    _name = 'omni.invoice'
    _description = 'OmniBilling Pro Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_invoice desc, id desc'

    name = fields.Char(string='Invoice Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    date_invoice = fields.Date(string='Invoice Date', default=fields.Date.context_today, required=True, tracking=True)
    date_due = fields.Date(string='Due Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    line_ids = fields.One2many('omni.invoice.line', 'invoice_id', string='Invoice Lines')
    transaction_ids = fields.One2many('omni.transaction', 'invoice_id', string='Transactions')
    
    amount_total = fields.Monetary(string='Total Amount', store=True, readonly=True, compute='_compute_amounts')
    amount_paid = fields.Monetary(string='Paid Amount', store=True, readonly=True, compute='_compute_amounts')
    amount_due = fields.Monetary(string='Amount Due', store=True, readonly=True, compute='_compute_amounts')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    notes = fields.Text(string='Terms and Conditions')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('omni.invoice') or _('New')
        return super().create(vals_list)

    @api.depends('line_ids.price_subtotal', 'transaction_ids.amount', 'transaction_ids.state')
    def _compute_amounts(self):
        for invoice in self:
            total = sum(invoice.line_ids.mapped('price_subtotal'))
            paid = sum(invoice.transaction_ids.filtered(lambda t: t.state == 'done').mapped('amount'))
            invoice.amount_total = total
            invoice.amount_paid = paid
            invoice.amount_due = total - paid
            
            if invoice.state == 'open' and invoice.amount_due <= 0 and total > 0:
                invoice.state = 'paid'

    def action_confirm(self):
        for record in self:
            if not record.line_ids:
                raise UserError(_("You cannot confirm an invoice without lines."))
            record.state = 'open'

    def action_register_payment(self):
        return {
            'name': _('Register Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'omni.transaction',
            'view_mode': 'form',
            'context': {
                'default_invoice_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_amount': self.amount_due,
            },
            'target': 'new',
        }

    def action_cancel(self):
        self.state = 'cancel'
        
    def action_draft(self):
        self.state = 'draft'


class OmniInvoiceLine(models.Model):
    _name = 'omni.invoice.line'
    _description = 'OmniBilling Invoice Line'

    invoice_id = fields.Many2one('omni.invoice', string='Invoice Reference', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    price_subtotal = fields.Monetary(string='Subtotal', store=True, readonly=True, compute='_compute_price_subtotal')
    currency_id = fields.Many2one(related='invoice_id.currency_id', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

class OmniTransaction(models.Model):
    _name = 'omni.transaction'
    _description = 'OmniBilling Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Transaction Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    invoice_id = fields.Many2one('omni.invoice', string='Invoice')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True, tracking=True)
    amount = fields.Monetary(string='Amount', required=True, tracking=True)
    currency_id = fields.Many2one(related='partner_id.currency_id', depends=['partner_id'], store=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit Card'),
        ('online', 'Online Payment Gateways'),
    ], string='Payment Method', default='bank', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('omni.transaction') or _('New')
        return super().create(vals_list)

    def action_confirm_payment(self):
        for record in self:
            record.state = 'done'
            if record.invoice_id:
                record.invoice_id._compute_amounts()
                
    def action_cancel(self):
        self.state = 'cancel'
