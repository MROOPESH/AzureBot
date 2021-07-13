# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            if turn_context.activity.text.lower() == 'yes':
                await dialog_context.begin_dialog(dialog.id)
                #await turn_context.send_activity("Employee Database...")
                #await turn_context.send_activity(dialog.id)

            else:
                await turn_context.send_activity("Have a Nice day!!!" + "\r\n" + "Type 'yes' to know details of employee..")
