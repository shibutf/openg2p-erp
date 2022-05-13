# -*- coding: utf-8 -*-
from odoo import fields, models, api


class DisenrollWizard(models.TransientModel):
    """
    A wizard to manage the creation/removal of disenrollment of users.
    """

    _name = "beneficiary.disenroll.wizard"
    _description = "Disenroll Into Program"

    program_id = fields.Many2one(
        "openg2p.program",
        string="Program",
        required=True,
    )
    # category_id = fields.Many2one(
    #     "openg2p.program.enrollment_category",
    #     string="Classification",
    # )
    date_end = fields.Date(
        "Disenroll Date",
        required=False,
        help="End Date of the program enrollment.",
    )
    use_active_domain = fields.Boolean("Use active domain")

    @api.multi
    def action_apply(self):
        beneficiary_obj = self.env["openg2p.beneficiary"]
        self.ensure_one()
        if self.use_active_domain:
            beneficiaries = beneficiary_obj.search(
                self.env.context.get("active_domain")
            )
        else:
            beneficiaries = beneficiary_obj.browse(self.env.context.get("active_ids"))

        if len(beneficiaries) > 1000:
            beneficiaries = beneficiaries.sudo().with_delay()

        for record in beneficiaries:
            existing_enrols = self.env["openg2p.program.enrollment"].search([("beneficiary_id","=",record.id),("program_id","=",self.program_id.id)])
            # the following size is one anyway
            for enrol in existing_enrols:
                disenrol_dict = {}
                disenrol_dict["state"] = "close"
                if self.date_end:
                    disenrol_dict["date_end"] = self.date_end
                enrol.write(disenrol_dict)
        return {"type": "ir.actions.act_window_close"}
