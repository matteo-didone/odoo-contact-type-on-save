# Contact Type on Save (Odoo 18)

In Odoo 18 the contact form sends `company_type` only, and `is_company` is set by its inverse after
the record is created. Constraints on stored fields run before that, so a new company can be checked
as an individual. This module sets `is_company` together with `company_type`, in `create` and `write`.

Reported in [odoo/odoo#283964](https://github.com/odoo/odoo/issues/283964) and
[OCA/l10n-italy#5182](https://github.com/OCA/l10n-italy/issues/5182). The same correction is proposed
to Odoo in [odoo/odoo#295861](https://github.com/odoo/odoo/pull/295861): once it is merged, uninstall
this module.

Check made stricter: an individual created where Odoo assumes a company (Invoicing) is now checked as
an individual.

## License

LGPL-3.0 or later.
