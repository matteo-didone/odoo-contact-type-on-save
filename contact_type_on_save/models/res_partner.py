# Copyright (C) 2026 Matteo Didone.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _add_is_company(self, vals):
        if vals.get("company_type") and "is_company" not in vals:
            return dict(vals, is_company=vals["company_type"] == "company")
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        return super().create([self._add_is_company(vals) for vals in vals_list])

    def write(self, vals):
        return super().write(self._add_is_company(vals))
