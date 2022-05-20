import os
import csv
import logging

from odoo import models

_logger = logging.getLogger(__name__)

beneficiary_base_id_type = os.getenv("PROGRAM_ENROLLMENT_ON_IMPORT_BENEFICIARY_BASE_ID", None)
beneficiary_base_id_label = os.getenv("PROGRAM_ENROLLMENT_ON_IMPORT_BENEFICIARY_BASE_ID_LABEL", "Related Base ID")


class BeneficiaryCSVReport(models.AbstractModel):
    _name = 'report.csv.beneficiary'
    _inherit = ['report.report_csv.abstract']
    _description = 'Beneficary csv report model'

    def _get_objs_for_report(self, docids, data):
        if data.get("use_active_domain", "false") == "true":
            active_domain = data.get("active_domain", [])
            return self.env[self.env.context.get('active_model')].search(active_domain)
        if docids:
            ids = docids
        elif data and 'context' in data:
            ids = data["context"].get('active_ids', [])
        else:
            ids = self.env.context.get('active_ids', [])
        return self.env[self.env.context.get('active_model')].browse(ids)
    
    def csv_report_options(self):
        res = super().csv_report_options()
        ben_fields = self.env["openg2p.beneficiary"]._fields
        res['fieldnames'].append(beneficiary_base_id_label)
        res['fieldnames'].append(ben_fields["program_ids"].string)
        res['delimiter'] = ','
        # res['quoting'] = csv.QUOTE_ALL
        return res

    def generate_csv_report(self, writer, data, partners):
        ben_fields = self.env["openg2p.beneficiary"]._fields
        writer.writeheader()
        for obj in partners:
            ben_base_id = ""
            for iden in obj.identities:
                if iden.category_id.code == beneficiary_base_id_type:
                    ben_base_id = iden.name
                    break
            programs_str = ", ".join([prog.name for prog in obj.program_ids])
            writer.writerow({
                beneficiary_base_id_label: ben_base_id,
                ben_fields["program_ids"].string: programs_str,
            })