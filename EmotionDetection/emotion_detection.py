import requests

def emotion_predict(text_to_analyze):
    """
    Envoie une requête à l'API Watson NLP pour détecter les émotions dans un texte.
    """
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        # Nouvelle gestion du status_code 400 :
        if response.status_code == 400:
            # Retourne un dict avec toutes les valeurs à None pour gérer l'entrée vide
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def emotion_detector(text_to_analyze):
    """
    Appelle emotion_predict et retourne un dictionnaire avec les scores d'émotion et l'émotion dominante.
    Gère également les entrées vides (None values) retournées en cas de status_code 400.
    """
    # Gestion entrée vide (optionnel si tu veux bloquer localement avant l'appel API)
    if not text_to_analyze or not text_to_analyze.strip():
        # Retour cohérent avec status_code 400
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    result = emotion_predict(text_to_analyze)
    
    if "error" in result:
        return result  # Erreur retournée par l'API

    # Si le dict retourné contient déjà les valeurs None (cas status_code 400)
    if all(value is None for value in result.values()):
        return result

    try:
        emotions = result['emotionPredictions'][0]['emotion']

        # Extraire les émotions importantes
        anger = emotions.get('anger', 0)
        disgust = emotions.get('disgust', 0)
        fear = emotions.get('fear', 0)
        joy = emotions.get('joy', 0)
        sadness = emotions.get('sadness', 0)

        emotion_scores = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }

        # Trouver l'émotion dominante
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        emotion_scores['dominant_emotion'] = dominant_emotion

        return emotion_scores

    except (KeyError, IndexError):
        return {"error": "Format de réponse inattendu depuis l'API."}

# Exemple d'utilisation
if __name__ == "__main__":
    text = "I am frustrated and angry about how things turned out."
    output = emotion_detector(text)
    print(output)
