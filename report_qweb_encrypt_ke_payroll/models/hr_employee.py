# Copyright 2026 Esidai / Hoteli
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    payroll_pdf_password = fields.Char(
        string="Payroll PDF password",
        help="Optional per-employee override for encrypted payslip and P9 "
        "PDFs. Leave empty to use the employee's national ID "
        "(identification number) instead.",
    )
