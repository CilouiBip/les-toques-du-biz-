# Les Toqués du Biz - Landing Page

## Guide d'ajout des images

### 1. Préparation des images

Placez vos images dans le dossier `images/` avec les spécifications suivantes :

#### Logo (`images/logo.png`)
- Dimensions : 240x80px
- Format : PNG avec transparence
- Taille max : 20KB
- Nom du fichier : `logo.png`

#### Image Hero (`images/hero.jpg`)
- Dimensions : 1200x800px
- Format : JPEG ou WebP
- Taille max : 200KB
- Nom du fichier : `hero.jpg`

#### Photo de profil (`images/mehdi.jpg`)
- Dimensions : 240x240px
- Format : JPEG ou WebP
- Taille max : 50KB
- Nom du fichier : `mehdi.jpg`

### 2. Optimisation des images

1. Ouvrez ImageOptim (installé dans Applications)
2. Glissez-déposez vos images
3. Attendez la fin de l'optimisation

### 3. Conversion WebP (optionnel mais recommandé)
```bash
cwebp -q 80 images/hero.jpg -o images/hero.webp
cwebp -q 85 images/mehdi.jpg -o images/mehdi.webp
```

### 4. Vérification
Une fois les images placées, ouvrez index.html dans votre navigateur pour vérifier que tout s'affiche correctement.

## Déploiement
1. Uploadez tout le dossier sur votre hébergeur
2. Remplacez l'URL du formulaire ConvertKit dans index.html
