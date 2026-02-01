"""
GameScene - Écran de jeu principal.
Gère le gameplay : fruits, bombes, glaçons, score, cœurs, freeze.
"""

import pygame
import os
from typing import List, Union, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, GameConfig, DIFFICULTY, FONT_FILE
)
from core import lang_manager
from core.scoring import ScoringManager, BonusGauge
from core.spawner import Spawner
from core.input_handler import InputHandler
from core.achievements import AchievementManager
from entities import Fruit, Bomb, Ice
from entities.splash import Splash
from ui.buttons import ImageButton


Entity = Union[Fruit, Bomb, Ice]


class GameScene(BaseScene):
    """Scène de jeu - mode classique et challenge."""
    
    # Taille de police pour le score
    SCORE_FONT_SIZE = 40
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.font_score = None
        self.font_letter = None
        
        # Images HUD
        self.coin_img = None  # TODO: ajouter l'image de la pièce
        self.heart_full_img = None
        self.heart_empty_img = None
        self.gauge_img = None
        self.gauge_segments = []  # [jaune, orange, rouge, violet, bleu]
        self.timer_frame_img = None  # Cadre du timer (challenge)
        
        # Boutons
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        
        # Composants
        self.scoring = ScoringManager()
        self.bonus_gauge = BonusGauge()
        self.spawner = None
        self.input_handler = None
        self.achievement_manager = None
        
        # État du jeu
        self.entities: List[Entity] = []
        self.splashes: List[Splash] = []  # Éclaboussures actives
        self.hearts = GameConfig.MAX_HEARTS
        self.game_time = 0.0
        self.is_frozen = False
        self.freeze_timer = 0.0
        self.game_over = False
        self.exploded = False  # Game over par bombe
        
        # Accumulation des fruits tranchés pendant un tracé souris
        self._stroke_sliced_fruits: List[Fruit] = []
        self._was_slicing = False
        
        # Mode de jeu
        self.mode = 'classic'  # 'classic' ou 'challenge'
        self.difficulty = 'normal'
        self.challenge_timer = 0.0
    
    def setup(self):
        """Initialise la partie."""
        # Récupérer les données du scene_manager
        self.mode = self.scene_manager.shared_data.get('mode', 'classic')
        self.difficulty = self.scene_manager.shared_data.get('difficulty', 'normal')
        control_mode = self.scene_manager.shared_data.get('control_mode', 'mouse')
        
        # Charger les ressources
        self._load_resources()
        
        # Initialiser les composants
        if self.mode == 'challenge':
            self.spawner = Spawner('challenge')
            self.challenge_timer = DIFFICULTY['challenge']['duration']
        else:
            self.spawner = Spawner(self.difficulty)
        
        self.input_handler = InputHandler(control_mode)
        
        # Reset état
        self.entities.clear()
        self.splashes.clear()
        self.scoring.reset()
        self.bonus_gauge.reset()
        self.hearts = GameConfig.MAX_HEARTS
        self.game_time = 0.0
        self.is_frozen = False
        self.freeze_timer = 0.0
        self.game_over = False
        self.exploded = False
        self._stroke_sliced_fruits.clear()
        self._was_slicing = False
        
        # Démarrer le tracking des succès
        if self.achievement_manager:
            self.achievement_manager.start_new_game(control_mode)
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Background selon le mode
        if self.mode == 'challenge':
            bg_path = os.path.join(IMAGES_DIR, Images.CHALLENGE_BG)
        else:
            bg_path = os.path.join(IMAGES_DIR, Images.GAME_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_score = pygame.font.Font(font_path, self.SCORE_FONT_SIZE)
        self.font_letter = pygame.font.Font(font_path, 24)
        
        # Cœurs
        self.heart_full_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.HEART_FULL)
        ).convert_alpha()
        self.heart_empty_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.HEART_EMPTY)
        ).convert_alpha()
        
        # Jauge
        self.gauge_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.GAUGE)
        ).convert_alpha()
        
        # Segments de la jauge
        segment_paths = [
            Images.GAUGE_YELLOW,
            Images.GAUGE_ORANGE,
            Images.GAUGE_RED,
            Images.GAUGE_PURPLE,
            Images.GAUGE_BLUE,
        ]
        self.gauge_segments = []
        for path in segment_paths:
            img = pygame.image.load(os.path.join(IMAGES_DIR, path)).convert_alpha()
            self.gauge_segments.append(img)
        
        # Cadre du timer (mode challenge uniquement)
        if self.mode == 'challenge':
            self.timer_frame_img = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.CHALLENGE_TIMER_FRAME)
            ).convert_alpha()
        
        # Boutons (engrenage et croix)
        self.btn_gear = ImageButton(
            image_path=Images.GEAR,
            center=Layout.GAME_GEAR,
            on_click=self._on_settings
        )
        self.btn_cross = ImageButton(
            image_path=Images.CROSS,
            center=Layout.GAME_CROSS,
            on_click=self._on_quit
        )
    
    def set_achievement_manager(self, manager: AchievementManager):
        """Définit le gestionnaire de succès."""
        self.achievement_manager = manager
    
    # Callbacks boutons
    def _on_settings(self):
        # TODO: ouvrir les paramètres en pause
        pass
    
    def _on_quit(self):
        # Retour au menu
        self.scene_manager.change_scene('menu')
    
    def handle_events(self, events: List[pygame.event.Event]):
        if self.game_over:
            return
        
        for event in events:
            # Boutons HUD
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            
            # Transmettre à l'input handler
            self.input_handler.handle_event(event)
            
            # Raccourci Échap pour quitter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._on_quit()
    
    def update(self, dt: float):
        if self.game_over:
            return
        
        self.game_time += dt
        
        # Mode challenge : décompte du temps
        if self.mode == 'challenge':
            self.challenge_timer -= dt
            if self.challenge_timer <= 0:
                self._end_game()
                return
        
        # Gestion du freeze
        if self.is_frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self._unfreeze_all()
        
        # Mise à jour du multiplicateur
        self.scoring.update(dt)
        
        # Spawn de nouvelles entités (sauf si freeze)
        if not self.is_frozen:
            keyboard_mode = self.input_handler.mode == "keyboard"
            new_entities = self.spawner.update(dt, keyboard_mode)
            self.entities.extend(new_entities)
        
        # Mise à jour des entités
        for entity in self.entities:
            entity.update(dt)
        
        # Mise à jour des éclaboussures
        for splash in self.splashes:
            splash.update(dt)
        
        # Détection des tranches
        sliced = self.input_handler.get_sliced_entities(self.entities)
        if sliced:
            self._process_sliced(sliced)
        
        # Vérifier fin de tracé souris pour calculer le score du combo
        is_slicing = self.input_handler.is_slicing()
        if self._was_slicing and not is_slicing:
            # Fin du tracé : calculer le score de tous les fruits accumulés
            self._finalize_stroke()
        self._was_slicing = is_slicing
        
        # Vérifier si le freeze doit se terminer (plus de fruits gelés)
        self._check_freeze_end()
        
        # Vérifier les entités sorties de l'écran
        self._check_missed_entities()
        
        # Nettoyer les entités mortes et les éclaboussures terminées
        self._cleanup_entities()
        self.splashes = [s for s in self.splashes if not s.finished]
        
        # Mise à jour du temps pour les succès
        if self.achievement_manager:
            self.achievement_manager.on_time_update(self.game_time)
    
    def _finalize_stroke(self):
        """Finalise un tracé souris : calcule le score et les bonus."""
        if not self._stroke_sliced_fruits:
            return
        
        fruits = self._stroke_sliced_fruits
        count = len(fruits)
        
        # Calculer les points (combo si plusieurs fruits)
        points = self.scoring.add_sliced_fruits(count)
        
        # Vérifier paires identiques pour la jauge bonus
        fruit_types = [f.fruit_type for f in fruits]
        for fruit_type in set(fruit_types):
            if fruit_types.count(fruit_type) >= 2:
                if self.bonus_gauge.add_cran():
                    self._activate_multiplier()
        
        # Succès
        if self.achievement_manager:
            self.achievement_manager.on_fruit_sliced(count)
            self.achievement_manager.on_score_update(self.scoring.score)
        
        # Reset pour le prochain tracé
        self._stroke_sliced_fruits.clear()
    
    def _process_sliced(self, sliced: List[Entity]):
        """Traite les entités tranchées."""
        fruits_sliced = []
        bomb_sliced = False
        ice_sliced = False
        
        for entity in sliced:
            entity.slice()
            
            # Libérer la lettre
            if entity.letter:
                self.spawner.release_letter(entity.letter)
            
            if isinstance(entity, Fruit):
                fruits_sliced.append(entity)
            elif isinstance(entity, Bomb):
                bomb_sliced = True
            elif isinstance(entity, Ice):
                ice_sliced = True
        
        # Priorité : bombe > glaçon > fruits (selon doc)
        if bomb_sliced:
            self._on_bomb_sliced()
            return
        
        if ice_sliced:
            self._on_ice_sliced()
        
        if fruits_sliced:
            self._on_fruits_sliced(fruits_sliced)
    
    def _on_fruits_sliced(self, fruits: List[Fruit]):
        """Appelé quand des fruits sont tranchés (accumule pour le tracé)."""
        # Créer les éclaboussures immédiatement
        for fruit in fruits:
            cx, cy = fruit.center
            splash = Splash(fruit.fruit_type, cx, cy)
            self.splashes.append(splash)
        
        # Mode souris : accumuler pour le combo de fin de tracé
        if self.input_handler.mode == "mouse":
            self._stroke_sliced_fruits.extend(fruits)
        else:
            # Mode clavier : traiter immédiatement (une touche = un groupe)
            count = len(fruits)
            self.scoring.add_sliced_fruits(count)
            
            # Vérifier paires identiques pour la jauge bonus
            fruit_types = [f.fruit_type for f in fruits]
            for fruit_type in set(fruit_types):
                if fruit_types.count(fruit_type) >= 2:
                    if self.bonus_gauge.add_cran():
                        self._activate_multiplier()
            
            # Succès
            if self.achievement_manager:
                self.achievement_manager.on_fruit_sliced(count)
                self.achievement_manager.on_score_update(self.scoring.score)
    
    def _on_bomb_sliced(self):
        """Appelé quand une bombe est tranchée."""
        if self.mode == 'challenge':
            # Mode challenge : pénalité de points
            penalty = DIFFICULTY['challenge']['bomb_penalty']
            self.scoring.apply_bomb_penalty(penalty)
        else:
            # Mode classique : game over instantané
            self.exploded = True
            self._end_game()
    
    def _on_ice_sliced(self):
        """Appelé quand un glaçon est tranché."""
        # Récupérer la durée du freeze selon la difficulté
        if self.mode == 'challenge':
            return  # Pas de glaçons en mode challenge
        
        freeze_duration = DIFFICULTY.get(self.difficulty, DIFFICULTY['normal']).get('freeze_duration', 4.0)
        self._freeze_all(freeze_duration)
        
        if self.achievement_manager:
            self.achievement_manager.on_ice_sliced()
    
    def _freeze_all(self, duration: float):
        """Gèle tous les fruits (pas les bombes ni les glaçons)."""
        self.is_frozen = True
        self.freeze_timer = duration
        
        # Ne geler que les fruits non tranchés
        for entity in self.entities:
            if isinstance(entity, Fruit) and not entity.sliced:
                entity.freeze()
    
    def _unfreeze_all(self):
        """Dégèle toutes les entités."""
        self.is_frozen = False
        self.freeze_timer = 0.0
        
        for entity in self.entities:
            if isinstance(entity, Fruit):
                entity.unfreeze()
    
    def _check_freeze_end(self):
        """Vérifie si le freeze doit se terminer (plus de fruits gelés)."""
        if not self.is_frozen:
            return
        
        # Compter les fruits encore gelés (non tranchés)
        frozen_fruits = [
            e for e in self.entities 
            if isinstance(e, Fruit) and e.frozen and not e.sliced
        ]
        
        if len(frozen_fruits) == 0:
            self._unfreeze_all()
    
    def _activate_multiplier(self):
        """Active le multiplicateur quand la jauge est pleine."""
        if self.scoring.has_multiplier:
            # Augmenter le multiplicateur existant
            self.scoring.increase_multiplier(
                BonusGauge.MULTIPLIER_INCREMENT,
                BonusGauge.MULTIPLIER_DURATION
            )
        else:
            # Premier multiplicateur
            self.scoring.activate_multiplier(2, BonusGauge.MULTIPLIER_DURATION)
    
    def _check_missed_entities(self):
        """Vérifie les entités sorties par le bas de la zone de jeu."""
        for entity in self.entities:
            if entity.sliced or entity.missed:
                continue
            
            # Un fruit est raté s'il sort par le bas de la zone de jeu
            if entity.y > GameConfig.GAME_ZONE_BOTTOM:
                entity.missed = True
                
                if isinstance(entity, Fruit):
                    self._on_fruit_missed()
                elif isinstance(entity, Bomb):
                    # Bombe évitée
                    if self.achievement_manager:
                        self.achievement_manager.on_bomb_avoided()
    
    def _on_fruit_missed(self):
        """Appelé quand un fruit est raté."""
        if self.mode == 'challenge':
            return  # Pas de pénalité en mode challenge
        
        self.hearts -= 1
        
        if self.achievement_manager:
            self.achievement_manager.on_heart_lost()
        
        if self.hearts <= 0:
            self._end_game()
    
    def _cleanup_entities(self):
        """Supprime les entités sorties de la zone de jeu."""
        self.entities = [
            e for e in self.entities
            if not (e.missed or e.y > GameConfig.GAME_ZONE_BOTTOM)
        ]
    
    def _end_game(self):
        """Termine la partie."""
        self.game_over = True
        
        # Finaliser les succès
        if self.achievement_manager:
            self.achievement_manager.end_game(self.exploded)
        
        # Sauvegarder le score
        self.scene_manager.shared_data['last_score'] = self.scoring.score
        self.scene_manager.shared_data['exploded'] = self.exploded
        # TODO: vérifier si nouveau record
        
        # Transition vers game over
        self.scene_manager.change_scene('game_over')
    
    def render(self, screen: pygame.Surface):
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Définir la zone de clip pour les entités (zone de jeu uniquement)
        game_zone_rect = pygame.Rect(
            GameConfig.GAME_ZONE_LEFT,
            GameConfig.GAME_ZONE_TOP,
            GameConfig.GAME_ZONE_SIZE[0],
            GameConfig.GAME_ZONE_SIZE[1]
        )
        screen.set_clip(game_zone_rect)
        
        # Éclaboussures (en arrière-plan des entités)
        for splash in self.splashes:
            splash.render(screen)
        
        # Entités (clippées à la zone de jeu)
        for entity in self.entities:
            entity.render(screen, self.font_letter if self.input_handler.mode == "keyboard" else None)
        
        # Traînée souris (clippée aussi)
        if self.input_handler.mode == "mouse" and self.input_handler.is_slicing():
            self._render_trail(screen)
        
        # Retirer le clip pour le reste du HUD
        screen.set_clip(None)
        
        # HUD (pas clippé)
        self._render_hud(screen)
    
    def _render_trail(self, screen: pygame.Surface):
        """Affiche la traînée de la souris."""
        points = self.input_handler.get_trail_points()
        if len(points) < 2:
            return
        
        # Ligne blanche avec effet de fade
        for i in range(1, len(points)):
            alpha = int(255 * (i / len(points)))
            color = (255, 255, 255)
            pygame.draw.line(screen, color, points[i-1], points[i], 3)
    
    def _render_hud(self, screen: pygame.Surface):
        """Affiche le HUD (score, cœurs/timer, jauge, boutons)."""
        # Score (haut gauche, justifié gauche depuis position 361)
        self._render_score(screen)
        
        # Cœurs ou Timer (haut centre)
        if self.mode == 'challenge':
            self._render_timer(screen)
        else:
            self._render_hearts(screen)
        
        # Boutons (haut droit)
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
        
        # Jauge bonus (bas centre)
        self._render_gauge(screen)
    
    def _render_score(self, screen: pygame.Surface):
        """Affiche le score avec multiplicateur si actif."""
        # Format: "140387 x2 (10s)" ou juste "140387"
        score_text = f"{self.scoring.score}"
        
        if self.scoring.has_multiplier:
            score_text += f" x{self.scoring.multiplier}"
            timer_left = int(self.scoring.multiplier_timer)
            score_text += f" ({timer_left}s)"
        
        score_surface = self.font_score.render(score_text, True, TextColors.GAME_SCORE)
        
        # Même position pour classic et challenge (justifié gauche)
        score_rect = score_surface.get_rect(left=Layout.GAME_SCORE_POS_CLASSIC[0], centery=Layout.GAME_SCORE_POS_CLASSIC[1])
        screen.blit(score_surface, score_rect)
    
    def _render_hearts(self, screen: pygame.Surface):
        """Affiche les 3 cœurs (mode classique)."""
        heart_positions = [
            Layout.GAME_HEART_1,
            Layout.GAME_HEART_2,
            Layout.GAME_HEART_3,
        ]
        
        for i, pos in enumerate(heart_positions):
            if i < self.hearts:
                img = self.heart_full_img
            else:
                img = self.heart_empty_img
            
            rect = img.get_rect(center=pos)
            screen.blit(img, rect)
    
    def _render_timer(self, screen: pygame.Surface):
        """Affiche le timer avec son cadre (mode challenge)."""
        # Cadre du timer
        if self.timer_frame_img:
            frame_rect = self.timer_frame_img.get_rect(center=Layout.GAME_TIMER)
            screen.blit(self.timer_frame_img, frame_rect)
        
        # Texte du timer
        minutes = int(self.challenge_timer) // 60
        seconds = int(self.challenge_timer) % 60
        timer_text = f"{minutes}:{seconds:02d}"
        
        timer_surface = self.font_score.render(timer_text, True, TextColors.GAME_SCORE)
        timer_rect = timer_surface.get_rect(center=Layout.GAME_TIMER)
        screen.blit(timer_surface, timer_rect)
    
    def _render_gauge(self, screen: pygame.Surface):
        """Affiche la jauge de bonus avec ses segments."""
        # Fond de la jauge
        gauge_rect = self.gauge_img.get_rect(center=Layout.GAME_GAUGE)
        screen.blit(self.gauge_img, gauge_rect)
        
        # Segments remplis selon le niveau de la jauge
        crans = self.bonus_gauge.crans
        for i in range(crans):
            if i < len(self.gauge_segments):
                segment_img = self.gauge_segments[i]
                segment_pos = Layout.GAME_GAUGE_SEGMENTS[i]
                segment_rect = segment_img.get_rect(center=segment_pos)
                screen.blit(segment_img, segment_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        self.entities.clear()
        if self.input_handler:
            self.input_handler.reset()
