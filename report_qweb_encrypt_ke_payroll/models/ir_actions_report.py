# Copyright 2026 Esidai / Hoteli
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _get_pdf_password(self, res_ids):
        """Resolve the encryption password with elevated rights.

        The password is derived from private HR data (per-employee
        override, national ID) that senders without HR read access
        (e.g. personal accounts triggering payslip mail) may not read
        directly. Resolving it here as sudo is safe: the value never
        leaves the server, it only locks a PDF the recipient is
        already authorized to receive.
        """
        return super(
            IrActionsReport, self.sudo()
        )._get_pdf_password(res_ids)
