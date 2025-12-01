# 🎨 Color Harmony Generator

**Color Harmony Generator** est une application conçue pour les designers et les développeurs. Elle permet de générer, visualiser et exporter des palettes de couleurs harmonieuses instantanément.
L'application combine la **théorie des couleurs** (pour les harmonies mathématiques) et le **Machine Learning** (pour l'extraction de couleurs d'images).

---

## Fonctionnalités

### 1. Génération via Couleur (Hex)
Entrez un code couleur (ex: `#3498db`) et obtenez les harmonies classiques :
-  **Complémentaire**
-  **Triadique**
-  **Analogique**
-  **Pastel**
-  **Monochrome**

### 2. Extraction via Image (AI)
Importez une image et laissez l'algorithme **K-Means (Clustering)** analyser les pixels pour en extraire les teintes dominantes et créer une palette cohérente.

### 3. Mode Aléatoire
En panne d'inspiration ? Générez une palette esthétique aléatoire en un clic.

### 4. Interface (GUI)
-   Support natif du **Dark Mode** et Light Mode.
-   Prévisualisation en temps réel.

### 5. Exportation
Sauvegardez vos palettes favorites sous forme d'images (PNG) haute définition prêtes à être partagées ou intégrées dans des maquettes.

---

## Installation

Assurez-vous d'avoir **Python 3.x** installé sur votre machine.

 **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

---

## Utilisation

Pour lancer l'interface graphique :

```bash
python main.py
