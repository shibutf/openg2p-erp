import csv
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class BeneficiaryCSVReport(models.AbstractModel):
    _name = 'report.csv.program.enrollment'
    _inherit = ['report.report_csv.abstract']
    _description = 'Program Enrollment csv report model'

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
        prog_enroll_fields = self.env["openg2p.program.enrollment"]._fields
        res['fieldnames'].append(prog_enroll_fields["related_ben_base_id"].string)
        res['fieldnames'].append(prog_enroll_fields["program_id"].string)
        res['fieldnames'].append(prog_enroll_fields["date_start"].string)
        res['fieldnames'].append(prog_enroll_fields["date_end"].string)
        res['fieldnames'].append(prog_enroll_fields["program_amount"].string)
        res['fieldnames'].append(prog_enroll_fields["total_amount"].string)
        res['fieldnames'].append(prog_enroll_fields["state"].string)
        res['delimiter'] = ','
        # res['quoting'] = csv.QUOTE_ALL
        return res

    def generate_csv_report(self, writer, data, partners):
        prog_enroll_fields = self.env["openg2p.program.enrollment"]._fields
        state_sel_dict = dict(prog_enroll_fields["state"].selection)
        writer.writeheader()
        for obj in partners:
            writer.writerow({
                prog_enroll_fields["related_ben_base_id"].string: obj.related_ben_base_id,
                prog_enroll_fields["program_id"].string: obj.program_id.name,
                prog_enroll_fields["date_start"].string: obj.date_start,
                prog_enroll_fields["date_end"].string: obj.date_end,
                prog_enroll_fields["program_amount"].string: obj.program_amount,
                prog_enroll_fields["total_amount"].string: obj.total_amount,
                prog_enroll_fields["state"].string: state_sel_dict[obj.state],
            })