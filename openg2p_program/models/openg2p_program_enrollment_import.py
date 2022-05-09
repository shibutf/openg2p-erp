import os
import logging
import itertools

from odoo import api, models, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

should_create_beneficiary = os.getenv("PROGRAM_ENROLLMENT_ON_IMPORT_SHOULD_CREATE_BENEFICIARY","false")
beneficiary_base_id_type = os.getenv("PROGRAM_ENROLLMENT_ON_IMPORT_BENEFICIARY_BASE_ID", None)


class ProgramEnrollmentImport(models.Model):
    _inherit = "openg2p.program.enrollment"

    program_ammount = fields.Float(
        string="Ammount", required=False, default=0.0
    )
    total_ammount = fields.Float(
        string="Total Remuneration", required=False, default=0.0
    )


    @api.multi
    def import_models(self, fields, columns, options, data_generator, dryrun=False):
        all_data = list(data_generator)
        columns = all_data[0]
        ben_base_id_cat = None
        if beneficiary_base_id_type:
            ben_base_id_cat = self.env["openg2p.beneficiary.id_category"].search([("code", "=", beneficiary_base_id_type)], limit=1)
            if not ben_base_id_cat or ben_base_id_cat.name not in columns:
                return {
                    'messages': [{
                        'type': 'error',
                        'message': 'Improperly Configured on import base Id. Or Base Id not found in Data',
                        'record': False,
                    }]
                }
        
        ben_error_count = 0
        ben_merge_count = 0
        ben_create_count = 0
        enrol_error_count = 0
        enrol_merge_count = 0
        enrol_create_count = 0
        total_count = 0
        error_messages = []
        success_ids = []
        for row in all_data[1:]:
            total_count += 1
            row_data = dict(zip(columns, row))

            program_name = row_data[self._fields["program_id"].string]
            enrol_date_start = row_data[self._fields["date_start"].string]
            enrol_date_end = row_data[self._fields["date_end"].string]
            enrol_program_ammount = row_data[self._fields["program_ammount"].string]
            enrol_total_ammount = row_data[self._fields["total_ammount"].string]
            enrol_state = row_data[self._fields["state"].string]

            existing_bens = None

            # checking if beneficiary exists and creating if required
            if beneficiary_base_id_type:
                ben_id_from_data = row_data[ben_base_id_cat.name]
                existing_bens = self.env["openg2p.beneficiary.id_number"].search([("name", "=", ben_id_from_data),("category_id","=", ben_base_id_cat.id)])
                if len(existing_bens) == 0 and should_create_beneficiary != "true":
                    error_messages.append({
                        'type': 'error',
                        'message': 'Beneficiary not found',
                        'record': str(row_data)
                    })
                    ben_error_count += 1
                    continue
                elif len(existing_bens) == 0 and should_create_beneficiary == "true":
                    try:
                        existing_bens = self.create_ben_with_data(ben_id_from_data, ben_base_id_cat, row_data)
                        ben_create_count += 1
                    except Exception as e:
                        error_messages.append({
                            'type': 'error',
                            'message': 'Error Creating Beneficiary: ' + str(e),
                            'record': str(row_data)
                        })
                        ben_error_count += 1
                elif len(existing_bens) == 1 and should_create_beneficiary == "true":
                    try:
                        self.merge_ben_with_data(existing_bens, row_data)
                        ben_merge_count += 1
                    except Exception as e:
                        error_messages.append({
                            'type': 'error',
                            'message': 'Error merging Beneficiary: ' + str(e),
                            'record': str(row_data)
                        })
                        ben_error_count += 1
                elif len(existing_bens) == 1:
                    pass
                # else len(existing_bens) is >1 or <0
                else:
                    raise ValidationError("Improper Beneficiary Data found in db")
            
            # checking if the current program enrollment exists and creating/merging accordingly
            program_id = self.env["openg2p.program"].search([("name", "=", program_name)], limit=1)
            existing_enrols = self.search([("program_id", "=", program_id.id),("beneficiary_id", "=", existing_bens.beneficiary_id.id)])
            if len(existing_enrols) == 0:
                try:
                    enrol = self.create({
                        "program_id": program_id.id,
                        "beneficiary_id": existing_bens.beneficiary_id.id,
                        "date_start": enrol_date_start,
                        "date_end": enrol_date_end if enrol_date_end else program_id.date_end,
                        "program_ammount": enrol_program_ammount,
                        "total_ammount": enrol_total_ammount,
                        "state": self.get_state_key_from_value(enrol_state)
                    })
                    success_ids.append(enrol.id)
                    enrol_create_count += 1
                except Exception as e:
                    error_messages.append({
                        'type': 'error',
                        'message': str(e),
                        'record': str(row_data)
                    })
                    enrol_error_count += 1
            elif len(existing_enrols) == 1:
                try:
                    existing_enrols.write({
                        "program_id": program_id.id,
                        "beneficiary_id": existing_bens.beneficiary_id.id,
                        "date_start": enrol_date_start,
                        "date_end": enrol_date_end if enrol_date_end else program_id.date_end,
                        "program_ammount": enrol_program_ammount,
                        "total_ammount": enrol_total_ammount,
                        "state": self.get_state_key_from_value(enrol_state)
                    })
                    success_ids.append(existing_enrols.id)
                    enrol_merge_count += 1
                except Exception as e:
                    error_messages.append({
                        'type': 'error',
                        'message': str(e),
                        'record': str(row_data)
                    })
                    enrol_error_count += 1
            # else len(existing_enrols) is >1 or <0
            else:
                raise ValidationError("Improper Program Enrollments found in db")

        # return super(ProgramEnrollmentImport, self).do(fields, columns, options, dryrun)
        _logger.info("Import Complete. Total Records Updated: %d. Enrollments Created: %d. Enrollments Merged: %d. Error Enrollments: %d. Beneficaries Created: %d. Beneficaries Merged: %d. Error Beneficaries: %d." % (total_count, enrol_create_count, enrol_merge_count, enrol_error_count, ben_create_count, ben_merge_count, ben_error_count))
        response = {
            'messages': error_messages
        }
        if len(success_ids)>0:
            response['ids'] = success_ids
        return response

    def create_ben_with_data(self, ben_base_id, ben_base_id_cat, row_data):
        display_name = row_data[self._fields["beneficiary_id"].string]
        first_name = display_name.split(" ", 1)[0]
        last_name = display_name.split(" ", 1)[1].split(" (", 1)[0]
        street = row_data["street"]
        city = row_data[self.env["openg2p.beneficiary"]._fields["city"].string]
        state = row_data[self.env["openg2p.beneficiary"]._fields["state_id"].string]
        country = row_data[self.env["openg2p.beneficiary"]._fields["country_id"].string]
        country_id = self.env["res.country"].search([("name", "=", country)], limit=1).id
        state_id = self.env["res.country.state"].search([("name", "=", state), ("country_id", "=", country_id)], limit=1).id
        data = {
            "firstname": first_name,
            "lastname": last_name,
            "street": street,
            "city": city,
            "state_id": state_id,
            "country_id": country_id,
        }
        ben = self.env["openg2p.beneficiary"].create(data)
        if beneficiary_base_id_type:
            return self.env["openg2p.beneficiary.id_number"].create(
                {
                    "name": ben_base_id,
                    "category_id": ben_base_id_cat.id,
                    "beneficiary_id": ben.id
                }
            )
        
        return None

    def merge_ben_with_data(self, existing_ben_base_id, row_data):
        display_name = row_data[self._fields["beneficiary_id"].string]
        first_name = display_name.split(" ", 1)[0]
        last_name = display_name.split(" ", 1)[1].split(" (", 1)[0]
        street = row_data["street"]
        city = row_data[self.env["openg2p.beneficiary"]._fields["city"].string]
        state = row_data[self.env["openg2p.beneficiary"]._fields["state_id"].string]
        country = row_data[self.env["openg2p.beneficiary"]._fields["country_id"].string]
        country_id = self.env["res.country"].search([("name", "=", country)], limit=1).id
        state_id = self.env["res.country.state"].search([("name", "=", state), ("country_id", "=", country_id)], limit=1).id
        data = {
            "firstname": first_name,
            "lastname": last_name,
            "street": street,
            "city": city,
            "state_id": state_id,
            "country_id": country_id,
        }
        existing_ben_base_id.beneficiary_id.write(data)
        return existing_ben_base_id
    
    def get_state_key_from_value(self, value):
        for k,v in self._fields["state"].selection:
            if v == value:
                return k
        return None