import argparse

import requests


def fetch_training_phrases(intent_name, text_type):
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(url)
    return response.json()[intent_name][text_type]


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
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--project-id",
        help="Project/agent id.  Required.",
        default='ogeko-mfcu',
    )
    parser.add_argument(
        "--intent",
        type=str,
        help='name of intent for training DF',
        default='Забыл пароль',
    )

    args = parser.parse_args()

    training_phrases_parts = fetch_training_phrases(
        args.intent,
        'questions',
    )
    message_texts = fetch_training_phrases(
        args.intent,
        'answer',
    )

    create_intent(
        args.project_id,
        args.intent,
        training_phrases_parts,
        [message_texts],
    )
