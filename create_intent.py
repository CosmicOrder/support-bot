import argparse
import os

import requests
from dotenv import load_dotenv
from requests import HTTPError


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

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

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "project-id",
        help="Project/agent id.  Required.",
    )

    args = parser.parse_args()

    URL = os.getenv('URL')

    response = requests.get(URL)
    response.raise_for_status()

    intents_in_json = response.json()

    for intent in intents_in_json:
        training_phrases_parts = intents_in_json[intent]['questions']
        message_texts = intents_in_json[intent]['answer']

        create_intent(
            args.project_id,
            intent,
            training_phrases_parts,
            [message_texts],
        )
