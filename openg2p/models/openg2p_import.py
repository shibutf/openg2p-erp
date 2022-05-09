import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class OpenG2pBaseImport(models.TransientModel):
    _inherit = "base_import.import"

    @api.multi
    def do(self, fields, columns, options, dryrun=False):
        _logger.info("Base import called.")
        if callable(getattr(self.env[self.res_model],"import_models", None)):
            data_gen = super(OpenG2pBaseImport, self)._read_file(options)
            return self.env[self.res_model].import_models(fields, columns, options, data_gen, dryrun)
        else:
            return super(OpenG2pBaseImport, self).do(fields, columns, options, dryrun)