# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile

from querydatalake import QueryDatalake

class UserProfileDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.empdetails_step,
                    self.empid_step,
                    self.summary_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        #    , UserProfileDialog.age_prompt_validator)
        #)
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        #self.add_dialog(
        #    AttachmentPrompt(
        #        AttachmentPrompt.__name__, UserProfileDialog.picture_prompt_validator
        #    )
        #)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def empdetails_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        # be run when the users response is received.
        # choices=[Choice("CurrentStatusoftheEmployee"), Choice("LocationoftheEmployee"), Choice("Departmentofthe")],
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Which of the below employee details you want?" + "\r\n" +"Click any one option below"),
                choices=[Choice("Current status"), Choice("Location of Employee"), Choice("Department")],
            ),
        )

    async def empid_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["empdetails"] = step_context.result.value

        return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter an Employee/Personal ID ."),
                    retry_prompt=MessageFactory.text(
                        "The value entered must be a valid Employee/Personal ID."
                    ),
                ),
        )
    """
    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        step_context.values["picture"] = (
            None if not step_context.result else step_context.result[0]
        )
        
        empid = step_context.result
        step_context.values["empid"] = empid 

        # WaterfallStep always finishes with the end of the Waterfall or
        # with another dialog; here it is a Prompt Dialog.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Is this ok?")),
        )
    """
    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        #if step_context.result:
        # Get the current profile object from user state.  Changes to it
        # will saved during Bot.on_turn.
        empid = step_context.result
        step_context.values["empid"] = empid 

        user_profile = await self.user_profile_accessor.get(
            step_context.context, UserProfile
        )
               

        user_profile.empdetails = step_context.values["empdetails"]
        user_profile.empid = step_context.values["empid"]
        qdl = QueryDatalake()
        ans = qdl.query_datalake(int(user_profile.empid), user_profile.empdetails)

        await step_context.context.send_activity(MessageFactory.text(ans))
        #user_profile.name = step_context.values["name"]
        #user_profile.age = step_context.values["age"]
        #user_profile.picture = step_context.values["picture"]
        """
        msg = f"I have your mode of transport as {user_profile.transport} and your name as {user_profile.name}."
        if user_profile.age != -1:
            msg += f" And age as {user_profile.age}."

        await step_context.context.send_activity(MessageFactory.text(msg))
        """

        """
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Thanks. Your profile will not be kept.")
            )
        """
        # WaterfallStep always finishes with the end of the Waterfall or with another
        # dialog, here it is the end.
        #await step_context.context.send_activity(MessageFactory.text("Would you like to know another details of the employee? Type yes/no…"))
        """
        await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Would you like to know another details of the employee?")),
        )        
        
        
        if step_context.result.value == "yes":
            return await step_context.begin_dialog()
        elif step_context.result == "NO":
            return await step_context.send_activity(MessageFactory.text("Have a Nice day :)"))
        """
        return await step_context.end_dialog()


    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        # This condition is our validation rule. You can also change the value at this point.
        return (
            prompt_context.recognized.succeeded
            and 0 < prompt_context.recognized.value < 150
        )


