import argparse
import os

import requests
from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == '__main__':
    load_dotenv()

    PROJECT_ID = os.getenv('PRODJECT_ID')
    URL = os.getenv('URL')

    response = requests.get(URL)
    response.raise_for_status()

    intents = response.json()

    for intent_name, phrases_parts in intents.items():
        for phrases_type, phrases in phrases_parts.items():
            if phrases_type == 'questions':
                training_phrases_parts = phrases
            elif phrases_type == 'answer':
                message_texts = phrases

        create_intent(
            PROJECT_ID,
            intent_name,
            training_phrases_parts,
            [message_texts],
        )
