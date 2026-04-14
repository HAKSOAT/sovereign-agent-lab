"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                                                              
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                                                                                     
2026-04-14 13:07:23 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said, "about 50 need vegan." The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So, the user is providing the number of vegan guests here.

First, I need to set the vegan_count slot. The user mentioned "about 50," so I should take that as the value. The slot expects a float, so even though it\'s "about," I\'ll input 50.0. 

Since the user is in the confirm_booking flow and has provided the vegan_count, the next step would be to ask for the deposit amount in GBP. The next slot to fill is deposit_amount_gbp, which is still undefined. So after setting vegan_count, the AI should prompt for the deposit amount. 

I need to make sure I only use the actions provided. So first, set the slot for vegan_count to 50.0, then start the next step in the confirm_booking flow by asking for deposit_amount_gbp. Wait, but the current step in the flow is already requesting vegan_count. Once that\'s set, the next requested slot would be deposit_amount_gbp. So the AI should automatically move to the next slot. Therefore, after setting vegan_count, the system should proceed to ask for the deposit amount. But according to the instructions, I need to output the actions based on the user\'s last message. The user provided the vegan_count, so the action is to set that slot. The next step would be the system\'s response, but maybe that\'s handled by the flow. So the only action needed here is setting the vegan_count to 50.0. Wait, the example shows that when a slot is filled, you set it. Since the user provided the value, the action is to set the slot. The flow will handle the next step. So the correct action here is to set the vegan_count to 50.0. No other actions are needed yet. Let me check the examples again. In the slot extraction example, when the user says "send money to John," they set the recipient and start the flow. Here, the flow is already active (confirm_booking), and the current step is asking for vegan_count. So the user\'s input fills that slot. Therefore, the action is to set slot vegan_count to 50.0. That\'s it. No need to start a flow again because it' message='No commands were parsed from the LLM actions.'
2026-04-14 13:07:23 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 guests need vegan                                                                                                                                                                                                              
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                                                                                            
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                                                              
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                                                                                     
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                                                                                                                                            
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                                                              
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                                                                                               
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  /stop 
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The agent was able to handle the out of scope request by immediately saying that it can only help with confirming tonight's venue booking, without spending further compute doing something else.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
The agent did not attempt to answer the out of scope request by calling a tool, instead it immediately said that it can only help with confirming tonight's venue booking. Unlike in the langraph response which tried to answer it, but only couldn't because there is no tool for train times.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I changed the following line in the actions.py file:

if now.hour > 16 or (now.hour == 16 and now.minute >= 45):

to:

if now.hour > 00 or (now.hour == 00 and now.minute >= 45):

As it was hour 16 previously, I changed it to 00 to test the cutoff guard.

Then I followed the regular conversation flow, and then the agent escalated. Otherwise I would have had to wait until 16:45 or later to test the cutoff guard.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
Python was handling the parsing of the user's input e.g. "about 160 people" → 160.0. In CALM, the LLM handles the parsing of the user's input.

Python is still handling the validation e.g validation of the guest count, vegan count, and deposit amount.

This is because LLMs should not be trusted to handle mathematical calculations or business rules.

The simplification cost is that a simple regex computation is now passed onto the LLM, which is compute intensive. However, it makes the implementation simpler.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The setup cost (more structure and more files) of the CALM agent is required to enforce structure and a more dependable workflow.

The CALM agent cannot try multiple paths like the LangGraph agent can. It can only follow the path defined in flows.yml, this means there is more trust in its execution.
"""
