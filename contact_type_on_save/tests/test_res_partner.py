# Copyright (C) 2026 Matteo Didone.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from unittest.mock import patch

from odoo import api
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartner(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, lang="en_US", tracking_disable=True))
        cls.Partner = cls.env["res.partner"]

    def _forbid_function_on_person(self):
        @api.constrains("function", "company_type")
        def _check(partners):
            for partner in partners:
                if partner.function and partner.company_type == "person":
                    raise ValidationError("person")

        return patch.object(type(self.Partner), "_constraint_methods", [_check])

    def test_create_company(self):
        with self._forbid_function_on_person():
            partner = self.Partner.create({"name": "A", "company_type": "company", "function": "X"})
        self.assertTrue(partner.is_company)

    def test_create_person_is_still_checked(self):
        with self._forbid_function_on_person(), self.assertRaises(ValidationError):
            self.Partner.create({"name": "A", "company_type": "person", "function": "X"})

    def test_create_default_is_company_then_person(self):
        with self._forbid_function_on_person(), self.assertRaises(ValidationError):
            self.Partner.with_context(default_is_company=True).create(
                {"name": "A", "company_type": "person", "function": "X"},
            )

    def test_write_company(self):
        partner = self.Partner.create({"name": "A"})
        with self._forbid_function_on_person():
            partner.write({"company_type": "company", "function": "X"})
        self.assertTrue(partner.is_company)

    def test_create_multi(self):
        partners = self.Partner.create([
            {"name": "A", "company_type": "company"},
            {"name": "B", "company_type": "person"},
            {"name": "C"},
            {"name": "D", "is_company": True},
        ])
        self.assertEqual(partners.mapped("is_company"), [True, False, False, True])

    def test_values_are_not_changed(self):
        vals = {"name": "A", "company_type": "company"}
        self.Partner.create(vals)
        self.assertNotIn("is_company", vals)

    def test_explicit_is_company_is_kept(self):
        vals = {"company_type": "person", "is_company": True}
        self.assertEqual(self.Partner._add_is_company(vals), vals)
