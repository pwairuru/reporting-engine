# Copyright 2026 Esidai / Hoteli
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "KE Payroll PDF Encryption Defaults",
    "summary": "Default encrypted payslip/P9 PDFs, national ID password",
    "version": "20.0.1.0.0",
    "license": "AGPL-3",
    "author": "Esidai",
    "website": "https://github.com/pwairuru/reporting-engine",
    "depends": [
        "report_qweb_encrypt",
        "hr_payroll_community",
        "l10n_ke_hr_payroll_community",
    ],
    "data": [
        "data/encrypt_defaults.xml",
        "views/hr_employee_views.xml",
        "views/portal_hints.xml",
    ],
    "installable": True,
}
