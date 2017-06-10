"""
This code sample is a part of a simple demo to show beginners how to create a skill (app) for the Amazon Echo using AWS Lambda and the Alexa Skills Kit.

For the full code sample visit https://github.com/pmckinney8/Alexa_Dojo_Skill.git
"""

from __future__ import print_function

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "VolcanoesList":
        return get_dojo_info_response()
    #elif intent_name == "VolcanoesDescription":
        #return get_dojo_staff_response()
    elif intent_name == "VolcanoesDescription":
        return get_dojo_stack_response(intent_request)
    elif intent_name == "VolcanoesHeight":
        return get_dojo_instructor_response(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Coding Dojo Skill. Great Job on getting started with your first skill. To get some examples of what this skill can do, ask for help now."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "Welcome to the help section for the Coding Dojo Skill. A couple of examples of phrases that I can except are... What is the coding dojo... or, who are the instructors. Lets get started now by trying one of these."

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_dojo_info_response():
    session_attributes = {}
    card_title = "Dojo_Info"
    speech_output = "The geography of Indonesia is dominated by volcanoes that are formed due to subduction zones between the Eurasian plate and the Indo-Australian plate. Some of the volcanoes are notable for their eruptions, for instance, Krakatau for its global effects in 1883,Lake Toba for its supervolcanic eruption estimated to have occurred 74,000 years before present which was responsible for six years of volcanic winter, and Mount Tambora for the most violent eruption in recorded history in 1815."

    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_dojo_staff_response():
    session_attributes = {}
    card_title = "Dojo_Staff"
    speech_output = "The Coding Dojo has a number of instructors at different locations. Our current locations are San Jose, Seattle, Burbank, Dallas, Washington DC, and Chicago. If you want information about a particular location you can ask the Coding Dojo skill. So for example you can ask... who are the instructors at the Chicago location."
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_dojo_stack_response(intent_request):
    session_attributes = {}
    card_title = "Dojo_Stack"
    speech_output = ""
    dojo_city = intent_request["intent"]["slots"]["Volcanoe"]["value"]

    if dojo_city == "Semeru":
        speech_output = "Semeru, or Mount Semeru (Indonesian: Gunung Semeru), is an active volcano located in East Java, Indonesia. It is the highest mountain on the island of Java. This stratovolcano is also known as Mahameru, meaning 'The Great Mountain.[1] The name derived from the Hindu-Buddhist mythical mountain of Meru or Sumeru, the abode of gods."
    elif dojo_city == "Rinjani":
        speech_output = "Mount Rinjani or Gunung Rinjani is an active volcano in Indonesia on the island of Lombok. Administratively the mountain is in the Regency of North Lombok, West Nusa Tenggara (Indonesian: Nusa Tenggara Barat, NTB). It rises to 3,726 metres (12,224 ft), making it the second highest volcano in Indonesia"
    elif dojo_city == "Klabat":
        speech_output = "Mount Klabat is the highest volcano on Sulawesi island, located in the east of Manado city, North Sulawesi, Indonesia. A 170 × 250 m wide, shallow crater lake is found at the summit. There are no confirmed historical eruptions of the volcano. A report of eruption taking place in 1683 is thought to have been produced by the Mount Tongkoko volcano instead."
    elif dojo_city == "Tidore":
        speech_output = "Tidore is a city, island, and archipelago in the Maluku Islands of eastern Indonesia, west of the larger island of Halmahera. In the pre-colonial era, the kingdom of Tidore was a major regional political and economic power, and a fierce rival of nearby Ternate, just to the north. Tidore Island consists of a large stratovolcano which rises from the seafloor to an elevation of 1,730 m (5,676 ft) above sea level at the conical Kiematabu Peak on the south end of the island. The northern side of the island contains a caldera, Sabale, with two smaller volcanic cones within it."
    else:
        speech_output = "Sorry, the Indonesia Volcanoes does not have an information that matches what you have asked for."
    reprompt_text = speech_output
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def get_dojo_instructor_response(intent_request):
    session_attributes = {}
    card_title = "Dojo_Stack"
    speech_output = ""
    dojo_city = intent_request["intent"]["slots"]["City"]["value"]

    if dojo_city == "Semeru":
        speech_output = "It is 3,676 metres (12,060 ft) high"
    elif dojo_city == "Rinjani":
        speech_output = "It is 3,726 metres (12,224 ft), making it the second highest volcano in Indonesia"
    elif dojo_city == "Klabat":
        speech_output = "It is 1,995 metres (6,545 ft)	high"
    elif dojo_city == "Tidore":
        speech_output = "It is 1,730 metres (5,680 ft) high"
    else:
        speech_output = "Indonesia Volcanoes does not have an information that matches what you have asked for."
    reprompt_text = speech_output
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Coding Dojo skill! We hope you enjoyed the experience."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
