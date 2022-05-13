# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProgramEnrollmentEnrollWizard(models.TransientModel):
    _name = "program.enrollment.enroll.wizard"
    _inherit = [ "beneficiary.enroll.wizard" ]

    @api.multi
    def action_apply(self):
        program_enrol_obj = self.env["openg2p.program.enrollment"]
        self.ensure_one()
        if self.use_active_domain:
            pre_existing_program_enrols = program_enrol_obj.search(
                self.env.context.get("active_domain")
            )
        else:
            pre_existing_program_enrols = program_enrol_obj.browse(self.env.context.get("active_ids"))

        if len(pre_existing_program_enrols) > 1000:
            pre_existing_program_enrols = pre_existing_program_enrols.sudo().with_delay()
        
        for record in pre_existing_program_enrols:
            enrol_exists = self.env["openg2p.program.enrollment"].search(
                [
                    ("beneficiary_id","=",record.beneficiary_id.id),
                    ("program_id","=",self.program_id.id),
                    ("state","=","open"),
                ], limit=1)
            if len(enrol_exists) == 0:
                record.beneficiary_id.program_enroll(
                    program_id=self.program_id.id,
                    #category_id=self.category_id.id,
                    date_start=self.date_start,
                    date_end=self.date_end if self.date_end else self.program_id.date_end,
                    program_amount=self.program_amount,
                    total_amount=self.total_amount,
                    confirm=self.auto_confirm,
                )
            elif len(enrol_exists) == 1:
                enrol_exists.write(
                    {
                        "date_start": self.date_start,
                        "date_end": self.date_end if self.date_end else self.program_id.date_end,
                        "program_amount": self.program_amount,
                        "total_amount": self.total_amount,
                    }
                )
        return {"type": "ir.actions.act_window_close"}