# Copyright 2020 Creu Blanca
# Copyright 2020 Ecosoft Co., Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from urllib.parse import parse_qsl

from odoo.http import request, route

from odoo.addons.web.controllers.report import ReportController


def _password_from_context(context):
    """Extract encrypt_password from a JSON-encoded context string."""
    if not context:
        return False
    try:
        return json.loads(context).get("encrypt_password", False)
    except (ValueError, AttributeError):
        return False


class ReportControllerEncrypt(ReportController):
    @route()
    def report_download(self, data, context=None, token=None, readonly=True):
        result = super().report_download(
            data, context=context, token=token, readonly=readonly
        )
        # When report is downloaded from print action, this function is called,
        # but this function cannot pass context (manually entered password) to
        # report.render_qweb_pdf(), encrypton for manual password is done here.
        if result.headers.get("Content-Type") != "application/pdf":
            return result
        request_content = json.loads(data)
        url, ttype = request_content[0], request_content[1]
        if ttype != "qweb-pdf":
            return result
        # Odoo 20 posts the user context separately and may also embed it
        # in the report URL query string (wizard reports). Check both.
        encrypt_password = _password_from_context(context)
        if not encrypt_password and "?" in url:
            # decoding the args represented in JSON
            args = dict(parse_qsl(url.split("?", 1)[1]))
            encrypt_password = _password_from_context(args.get("context"))
        if not encrypt_password:
            return result
        encrypted_data = request.env["ir.actions.report"]._encrypt_pdf(
            result.get_data(), encrypt_password
        )
        result.set_data(encrypted_data)
        return result
