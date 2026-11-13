# Copyright 2026 Esidai / Hoteli
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Encryption defaults for the two employee reports.

Covers: install-time report config, national-ID default password,
per-employee override precedence, encrypt on/off behaviour (roundtrip
through pypdf, no wkhtmltopdf needed), and the email/portal key hint.
"""
from io import BytesIO

from odoo.tests.common import TransactionCase
from odoo.tools.pdf import PdfReader, PdfWriter


def _sample_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue()


class TestKePayrollEncrypt(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.payslip_report = cls.env.ref(
            "hr_payroll_community.hr_payslip_report_action"
        )
        cls.p9_report = cls.env.ref(
            "l10n_ke_hr_payroll_community.action_ke_p9_individual_report"
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Encrypt Test", "identification_id": "NAT123"}
        )

    def _payslip(self):
        return self.env["hr.payslip"].create(
            {
                "name": "Test slip",
                "employee_id": self.employee.id,
                "date_from": "2026-01-01",
                "date_to": "2026-01-31",
            }
        )

    def test_reports_default_to_auto_encrypt(self):
        """Both employee reports ship encrypted, keyed on national ID."""
        for report in self.payslip_report | self.p9_report:
            self.assertEqual(report.encrypt, "auto")
            self.assertIn("identification_id", report.encrypt_password or "")

    def test_password_defaults_to_national_id(self):
        self.assertEqual(
            self.payslip_report._get_pdf_password([self._payslip().id]),
            "NAT123",
        )

    def test_employee_override_wins_over_national_id(self):
        self.employee.payroll_pdf_password = "OVERRIDE9"
        self.assertEqual(
            self.payslip_report._get_pdf_password([self._payslip().id]),
            "OVERRIDE9",
        )

    def test_p9_wizard_password_uses_employee(self):
        wizard = self.env["ke.p9.wizard"].create(
            {"year": 2026, "employee_id": self.employee.id}
        )
        self.assertEqual(
            self.p9_report._get_pdf_password([wizard.id]), "NAT123"
        )

    def test_no_password_means_open_pdf(self):
        """Empty override + empty national ID leaves the PDF unencrypted."""
        self.employee.write(
            {"payroll_pdf_password": False, "identification_id": False}
        )
        pdf = _sample_pdf()
        password = self.payslip_report._get_pdf_password(
            [self._payslip().id]
        )
        self.assertFalse(password)
        self.assertEqual(
            self.env["ir.actions.report"]._encrypt_pdf(pdf, password), pdf
        )

    def test_disabled_report_gives_open_pdf(self):
        """Admins can switch encryption off per report."""
        self.payslip_report.encrypt = False
        self.assertFalse(
            self.payslip_report._get_pdf_password([self._payslip().id])
        )

    def test_encrypt_roundtrip(self):
        pdf = _sample_pdf()
        encrypted = self.env["ir.actions.report"]._encrypt_pdf(
            pdf, "secret"
        )
        self.assertIn(b"/Encrypt", encrypted)
        reader = PdfReader(BytesIO(encrypted))
        self.assertTrue(reader.is_encrypted)
        self.assertNotEqual(reader.decrypt("secret"), 0)
        self.assertEqual(len(reader.pages), 1)

    def test_mail_template_tells_employee_the_key(self):
        template = self.env.ref("hr_payroll_community.email_template_payslip")
        self.assertIn("national ID", template.body_html)
        self.assertIn("password-protected", template.body_html.lower())
