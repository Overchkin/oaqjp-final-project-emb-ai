from flask import Flask, request, render_template
import sys
import os

# Ajouter le chemin du sous-dossier contenant emotion_detection.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'oaqjp-final-project-emb-ai'))

# Import de la fonction de détection des émotions
try:
    from EmotionDetection.emotion_detection import emotion_detector
    print("✅ Import réussi de emotion_detector")
except Exception as e:
    print(f"❌ Échec de l'import de emotion_detector : {e}")
    raise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'oaqjp-final-project-emb-ai', 'static')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'oaqjp-final-project-emb-ai', 'templates')

# Correction ici : préciser les chemins absolus des dossiers static et templates
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def emotion_route():
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return "Erreur: Aucun texte fourni", 400

    result = emotion_detector(text_to_analyze)

    if isinstance(result, dict) and "emotion" in result:
        emotions = result["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)
        response = (
            f"Le texte présente principalement l'émotion : {dominant_emotion} "
            f"(score : {emotions[dominant_emotion]:.2f})"
        )
        return response
    elif "error" in result:
        return f"Erreur de détection : {result['error']}", 500
    else:
        return "Erreur inattendue dans la réponse Watson NLP", 500

if __name__ == "__main__":
    app.run(debug=True)
