from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image
import json
import tempfile

app = Flask(__name__, static_folder='static')
app.secret_key = 'votre_clé_secrète_ici'  # Pour les messages flash et la session

# Configuration
TEMP_FOLDER = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_FOLDER, 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
CONFIG_FILE = os.path.join(TEMP_FOLDER, 'config.json')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que le dossier images existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'headline': "Scaler sans pleurer! Simplifiez, Accélérez, Répétez.",
        'intro': "15 ans d'expérience en opérations & scaling, de L'Oréal à Getir : j'aide les solopreneurs à grandir vite, sans complexité inutile.",
        'presentation1': "Salut, moi c'est Mehdi. Après 15 ans dans les opérations (L'Oréal, Yum, Getir, Mindeo & mes business), j'ai compris que la complexité tue la croissance.",
        'presentation2': "Dans Les Toqués du Biz, je partage mes astuces pour simplifier ton organisation, maximiser tes résultats et travailler (un peu) moins. Pas de bullshit, juste du concret.",
        'bullets': [
            "Fais plus avec moins : tes ventes montent, ta to-do diminue.",
            "Évite l'usine à gaz : finis les 10 000 outils ou 15 freelances à gérer.",
            "Boost anti-bullshit : je ne vends pas du rêve, juste du concret pour scaler sereinement.",
            "2-3 emails/semaine : courts, clairs, sans blabla, avec une pointe d'humour."
        ],
        'reassurance': "15 ans de terrain : J'ai dirigé des équipes jusqu'à 2 000 personnes et managé des P&L multimillionnaires. Maintenant, j'aide les solopreneurs à passer le cap du \"j'ai plus de temps\" sans embaucher 10 personnes.",
        'cta_button': "Oui, je veux des astuces concrètes !",
        'form_notice': "Bienvenue dans Les Toqués du Biz ! Regarde ta boîte mail pour confirmer.",
        'convertkit_url': "#"
    }

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_available_images():
    if not os.path.exists(UPLOAD_FOLDER):
        return []
    return [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]

@app.route('/')
def index():
    config = load_config()
    images = get_available_images()
    return render_template('index.html', config=config, images=images)

@app.route('/admin')
def admin():
    config = load_config()
    return render_template('admin.html', config=config)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Aucun fichier n\'a été envoyé')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('Aucun fichier n\'a été sélectionné')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Sauvegarder le fichier temporairement
        file.save(filepath)
        
        try:
            # Ouvrir et optimiser l'image
            with Image.open(filepath) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionner si l'image est trop grande
                max_size = (800, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.LANCZOS)
                
                # Sauvegarder avec une compression optimisée
                img.save(filepath, 'JPEG', quality=85, optimize=True)
            
            flash('Image téléchargée et optimisée avec succès')
        except Exception as e:
            flash(f'Erreur lors du traitement de l\'image: {str(e)}')
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('admin'))
        
        return redirect(url_for('admin'))
    
    flash('Type de fichier non autorisé')
    return redirect(url_for('admin'))

@app.route('/update_config', methods=['POST'])
def update_config():
    try:
        config = {
            'headline': request.form.get('headline', ''),
            'intro': request.form.get('intro', ''),
            'presentation1': request.form.get('presentation1', ''),
            'presentation2': request.form.get('presentation2', ''),
            'bullets': [
                request.form.get('bullet_0', ''),
                request.form.get('bullet_1', ''),
                request.form.get('bullet_2', ''),
                request.form.get('bullet_3', '')
            ],
            'reassurance': request.form.get('reassurance', ''),
            'cta_button': request.form.get('cta_button', ''),
            'form_notice': request.form.get('form_notice', ''),
            'convertkit_url': request.form.get('convertkit_url', '')
        }
        
        # Vérifier que les champs ne sont pas vides
        for key, value in config.items():
            if not value.strip():
                flash(f'Le champ {key} ne peut pas être vide')
                return redirect(url_for('admin'))
        
        save_config(config)
        flash('Configuration mise à jour avec succès')
        
    except Exception as e:
        flash(f'Erreur lors de la mise à jour de la configuration: {str(e)}')
    
    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
