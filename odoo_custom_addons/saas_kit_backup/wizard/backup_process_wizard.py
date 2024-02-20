# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api
from odoo.exceptions import UserError


CYCLE = [
    ('half_day', 'Twice a day'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]



class CreateBackupProcess(models.TransientModel):
    _name = 'backup.process.wizard'
    _description = "Backup Process Wizard"
    
    def _default_enable_retention(self):
        IrDefault = self.env['ir.default'].sudo()
        enable_retention = IrDefault._get('res.config.settings', 'enable_retention')
        return enable_retention
    
    def _default_retention_count(self):
        IrDefault = self.env['ir.default'].sudo()
        backup_retention_count = IrDefault._get('res.config.settings', 'backup_retention_count')
        return backup_retention_count
    
    
    
    name = fields.Char(string="Name")
    frequency = fields.Integer(string="Frequency", default=1)
    frequency_cycle = fields.Selection(selection=CYCLE, string="Backup Frequency", default="daily")
    storage_path = fields.Char(string="Storage Path")
    backup_starting_time = fields.Datetime(string="Backup Starting Date and Time")
    backup_format = fields.Selection([('zip', 'zip (includes filestore)'), ('dump', 'pg_dump custom format (without filestore)')], string="Backup Format", default="zip", help="Select the file format of the data backup file.") 
    enable_retention = fields.Boolean(string="Drop Old Backups", default=_default_enable_retention, help="Check if you want to drop old backups stored on the server.")
    retention = fields.Integer(string="Backup Retention Count", default=_default_retention_count, help="Count of recent backups that will be retained after dropping old backups on server.")
    
    
    @api.constrains('retention')
    def check_retention_value(self):
        """
            Method to check the value of retention field
        """

        if self.enable_retention:
            if self.retention < 1:
                raise UserError("Backup Retention Count should be at least 1.")

    def create_process_data(self):
        client_id = self._context['client_id']
        client_id = self.env['saas.client'].sudo().browse([client_id])
        if self.frequency_cycle == 'half_day':
            frequency = 2
        else:
            frequency = 1
        client_id.create_backup_process(frequency=frequency, frequency_cycle=self.frequency_cycle, backup_starting_time=self.backup_starting_time, backup_format=self.backup_format, enable_retention=self.enable_retention, retention=self.retention)


class CancelBackupPrcoessWizard(models.TransientModel):
    _name = 'cancel.backup.process'
    _description = "Cancel Backup Process Wizard"


    name = fields.Char(string="Name")
    purpose = fields.Selection(selection=[('cancel_backup', 'Cancel Backup')], string="Purpose")
    record_id = fields.Integer(string="Record Id")


    def call_record_method(self):
        res = self.env['saas.client'].sudo().search([('id', '=', self.record_id)])
        res.delete_backup_crone()
