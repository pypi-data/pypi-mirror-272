# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Inventory Closing Queue",
    "version": "14.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "queue_job_batch",
        "ssi_inventory_closing",
        "ssi_transaction_queue_done_mixin",
        "ssi_transaction_queue_cancel_mixin",
        "base_automation",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
    ],
    "demo": [],
    "images": [],
}
