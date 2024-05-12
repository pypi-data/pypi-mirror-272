# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, models

from odoo.addons.ssi_decorator import ssi_decorator


class InventoryClosing(models.Model):
    _inherit = [
        "mixin.transaction_queue_cancel",
        "mixin.transaction_queue_done",
        "inventory_closing",
    ]
    _name = "inventory_closing"

    _after_approved_method = "action_queue_done"
    _statusbar_visible_label = "draft,confirm,queue_done,done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _queue_processing_create_page = True
    _automatically_insert_queue_done_button = False
    _automatically_insert_queue_cancel_button = False

    _queue_to_done_insert_form_element_ok = True
    _queue_to_done_form_xpath = "//group[@name='queue_processing']"

    _queue_to_cancel_insert_form_element_ok = True
    _queue_to_cancel_form_xpath = "//group[@name='queue_processing']"

    _method_to_run_from_wizard = "action_queue_cancel"

    @ssi_decorator.post_queue_done_action()
    def _02_create_aml_from_svl_on_queue_done(self):
        self.ensure_one()
        for svl in self.stock_valuation_layer_ids:
            description = "Create AML From SVL ID %s" % (svl.id)
            svl.with_context(job_batch=self.done_queue_job_batch_id).with_delay(
                description=_(description)
            )._create_accounting_entry()

    @ssi_decorator.post_done_action()
    def _01_update_svl_journal(self):
        self.ensure_one()
        return True

    @ssi_decorator.post_done_action()
    def _02_create_aml_from_svl(self):
        self.ensure_one()
        return True

    @ssi_decorator.post_queue_done_action()
    def _01_update_svl_journal_on_queue_done(self):
        self.ensure_one()
        for move in self.stock_move_ids:
            if not move.journal_id:
                move.picking_id.write(
                    {
                        "journal_id": self.journal_id.id,
                    }
                )

    @ssi_decorator.post_cancel_action()
    def _01_delete_aml(self):
        self.ensure_one()
        return True

    @ssi_decorator.post_queue_cancel_action()
    def _01_delete_aml_on_queue_cancel(self):
        self.ensure_one()
        for svl in self.stock_valuation_layer_ids:
            description = "Delete AML From SVL ID %s" % (svl.id)
            svl.with_context(job_batch=self.cancel_queue_job_batch_id).with_delay(
                description=_(description)
            )._delete_accounting_entry()

    @api.model
    def _get_policy_field(self):
        res = super(InventoryClosing, self)._get_policy_field()
        policy_field = [
            "queue_done_ok",
            "queue_cancel_ok",
        ]
        res += policy_field
        return res
