# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProgramEnrollmentDisenrollWizard(models.TransientModel):
    _name = "program.enrollment.disenroll.wizard"
    _inherit = [ "beneficiary.disenroll.wizard" ]

    @api.multi
    def action_apply(self):
        program_enrollment_obj = self.env["openg2p.program.enrollment"]
        self.ensure_one()
        if self.use_active_domain:
            beneficiaries = program_enrollment_obj.search(
                self.env.context.get("active_domain")
            )
        else:
            program_enrols = program_enrollment_obj.browse(self.env.context.get("active_ids"))

        if len(program_enrols) > 1000:
            program_enrols = program_enrols.sudo().with_delay()

        for record in program_enrols:
            disenrol_dict = []
            disenrol_dict["state"] = "close"
            if self.date_end:
                disenrol_dict["date_end"] = self.date_end
            record.write(disenrol_dict)
        return {"type": "ir.actions.act_window_close"}
