<div align="center">

# RPG Village — Projet Jeux Python

<br>

> *Un RPG 2D top-down où un héros doit sauver le grand arbre de son village en éliminant la menace qui rôde au fond de la forêt.*

</div>

---

## Présentation

Le village est en danger. Le grand arbre — cœur de la communauté — dépérit à cause d'un monstre tapi dans les profondeurs du donjon.
Les habitants comptent sur toi : explore le village, parle aux PNJ, affronte les créatures et descends dans le donjon pour terrasser le Boss final.

---

## Fonctionnalités

| Fonctionnalité | Détail |
|---|---|
| **Exploration multi-cartes** | Village, maisons et donjon interconnectés via des portails |
| **Système de dialogues** | Conversations avec les PNJ |
| **Combat** | Gobelins, Slimes et un Boss final |
| **Système de vie** | Objets de soin et réceptacles de cœur (augmente le max HP) |
| **Caméra dynamique** | Centrée sur le joueur avec zoom x5 |
| **Collisions complètes** | Murs, PNJ, ennemis, objets ramassables |

---

## Structure du projet

```
PROJET_JEUX_PYTHON/
│
├── src/
│   ├── main.py          # Point d'entrée du jeu
│   ├── game.py          # Boucle principale
│   ├── map.py           # Gestion des cartes et portails
│   ├── player.py        # Joueur & PNJ
│   ├── enemy.py         # Ennemis : Goblin, Slime, Boss
│   ├── items.py         # Objets : soin, cœur
│   └── dialog.py        # Système de dialogue
│
└── assets/
    ├── map.tmx           # Village principal
    ├── house1.tmx
    ├── house1_room1.tmx
    ├── house2.tmx
    ├── house3.tmx
    └── dungeon.tmx       # Donjon du Boss
```

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-user/projet-jeux-python.git
cd projet-jeux-python
```

### 2. Installer les dépendances

```bash
pip install pygame pytmx pyscroll
```

### 3. Lancer le jeu

```bash
cd src
python main.py
```

---

## Contrôles

<div align="center">

| Touche | Action |
|:------:|--------|
| `↑` | Se déplacer vers le haut |
| `↓` | Se déplacer vers le bas |
| `←` | Se déplacer à gauche |
| `→` | Se déplacer à droite |
| `Espace` | Attaquer |
| `T` | Lancer le dialogue et l'avancer |

</div>

---

## Cartes

```
Village (map)
 ├── House 1
 │    └── Room 1
 ├── House 2  —  Maelys
 ├── House 3  —  Arthur
 └── Dungeon  —  Boss
```

---

## Bestiaire

<div align="center">

| Ennemi | Nombre | Zone |
|--------|:------:|------|
| Slime | 11 | Village |
| Goblin | 20 | Village |
| Boss | 1 | Donjon |

</div>

---

## PNJ

<div align="center">

| Nom | Zone | Rôle |
|-----|------|------|
| **Geaq** | Village | Accueil et orientation du joueur |
| **Rush Dark** | Village | Informe sur la menace dans la forêt |
| **Maelys** | House 2 | Indique le grand arbre |
| **Arthur** | House 3 | Personnage mystérieux |

</div>

---

## Technologies

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-00B140?style=flat-square&logo=python&logoColor=white)](https://www.pygame.org/)
[![PyTMX](https://img.shields.io/badge/PyTMX-chargement%20cartes-lightgrey?style=flat-square)](https://github.com/bitcraft/pytmx)
[![Pyscroll](https://img.shields.io/badge/Pyscroll-rendu%20cartes-lightgrey?style=flat-square)](https://github.com/bitcraft/pyscroll)
[![Tiled](https://img.shields.io/badge/Tiled-Map%20Editor-20B2AA?style=flat-square)](https://www.mapeditor.org/)

</div>

---

## Auteurs

Projet réalisé dans le cadre du cours **Projets Transversaux POO** — *EPSI B1*.

---

<div align="center">

*Ce projet est à usage éducatif.*

</div>
