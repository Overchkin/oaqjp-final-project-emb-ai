"""
Module server.py
Application Flask pour détecter les émotions à partir d'un texte donné.
"""

from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """
    Route principale qui renvoie la page d'accueil.
    
    Returns:
        str: Contenu HTML de la page index.html.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    Route qui traite la requête d'analyse d'émotion.
    Récupère le texte à analyser via GET ou POST, appelle la fonction emotion_detector,
    puis renvoie la réponse formatée ou un message d'erreur si nécessaire.
    
    Returns:
        str: Résultat de l'analyse émotionnelle ou message d'erreur.
    """
    text = request.args.get('textToAnalyze') or request.form.get('text')

    if not text:
        return "Texte invalide ! Veuillez réessayer !"

    result = emotion_detector(text)

    if "error" in result:
        response = f"Erreur lors de l’analyse : {result['error']}"
    elif result.get('dominant_emotion') is None:
        response = "Texte invalide ! Veuillez réessayer !"
    else:
        response = (
            f"Pour l'énoncé donné, la réponse du système est "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} et "
            f"'sadness': {result['sadness']}. "
            f"L'émotion dominante est {result['dominant_emotion']}."
        )

    return response


if __name__ == '__main__':
    app.run(debug=True)
