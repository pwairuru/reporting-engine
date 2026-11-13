KE Payroll PDF Encryption Defaults
====================================

Encrypts employee payslip and individual P9 PDFs by default, using the
generic ``report_qweb_encrypt`` mechanism (any other QWeb PDF report can be
locked the same way via Settings > Technical > Reports).

* Password: per-employee ``Payroll PDF password`` override, else the
  employee's national ID (``identification_id``).
* Encryption can be switched off per report (set ``Encryption`` to empty on
  the report action); a report with no resolvable password stays open, so
  employees without a national ID on file are never locked out.
* The payslip email template and the portal download pages tell the
  employee which key opens the PDF.
* The all-employees P9 summary has no single employee and stays unencrypted.
