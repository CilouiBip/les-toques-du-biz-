from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image
import json

app = Flask(__name__, static_folder='assets')
app.secret_key = 'votre_clé_secrète_ici'  # Pour les messages flash et la session

# Configuration
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
CONFIG_FILE = 'config.json'

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
    images = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images.append(filename)
    return images

@app.route('/')
def index():
    config = load_config()
    config['images'] = get_available_images()
    return render_template('index.html', **config)

@app.route('/admin')
def admin():
    config = load_config()
    return render_template('admin.html', config=config)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('Pas de fichier')
        return redirect(request.url)
    
    file = request.files['image']
    image_type = request.form.get('type')
    
    if file.filename == '':
        flash('Pas de fichier sélectionné')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Définir le nom de fichier en fonction du type
        if image_type == 'logo':
            filename = 'logo.png'
        elif image_type == 'hero':
            filename = 'hero.jpg'
        elif image_type == 'profile':
            filename = 'mehdi.jpg'
        else:
            flash('Type d\'image invalide')
            return redirect(url_for('admin'))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Sauvegarder et optimiser l'image
        img = Image.open(file)
        
        # Redimensionner selon le type
        if image_type == 'logo':
            img = img.resize((240, 80), Image.Resampling.LANCZOS)
        elif image_type == 'hero':
            img = img.resize((1200, 800), Image.Resampling.LANCZOS)
        elif image_type == 'profile':
            img = img.resize((240, 240), Image.Resampling.LANCZOS)
        
        # Sauvegarder avec optimisation
        img.save(filepath, optimize=True, quality=85)
        
        flash(f'Image {filename} uploadée avec succès')
        return redirect(url_for('admin'))

@app.route('/update_config', methods=['POST'])
def update_config():
    config = load_config()
    
    # Mettre à jour les champs texte
    fields = ['headline', 'intro', 'presentation1', 'presentation2', 'reassurance', 
              'cta_button', 'form_notice', 'convertkit_url']
    
    for field in fields:
        if field in request.form:
            config[field] = request.form[field]
    
    # Mettre à jour les bullets
    bullets = []
    for i in range(4):  # Supposons qu'il y a toujours 4 bullets
        bullet_key = f'bullet_{i}'
        if bullet_key in request.form:
            bullets.append(request.form[bullet_key])
    config['bullets'] = bullets
    
    save_config(config)
    flash('Configuration mise à jour avec succès')
    return redirect(url_for('admin'))

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=9000, debug=True)
