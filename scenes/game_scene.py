"""
GameScene - Écran de jeu principal.
Gère le gameplay : fruits, bombes, glaçons, score, cœurs, freeze.
Inclut le système d'états de Yoshi qui réagit aux événements.
"""

import pygame
import os
from typing import List, Union, Optional
from enum import Enum

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, GameConfig, DIFFICULTY, FONT_FILE
)
from core import lang_manager
from core import audio_manager
from core.scoring import ScoringManager, BonusGauge
from core.spawner import Spawner
from core.input_handler import InputHandler
from core.achievements import AchievementManager
from entities import Fruit, Bomb, Ice
from entities.splash import Splash
from ui.buttons import ImageButton


Entity = Union[Fruit, Bomb, Ice]


class YoshiState(Enum):
    """États possibles de Yoshi pendant le jeu."""
    ATTEND = "attend"      # Par défaut
    CONTENT = "content"    # Combo réussi
    TRISTE = "triste"      # Perte de cœur ou bombe en challenge
    AFFAME = "affame"      # 1 cœur restant (classique seulement)
    GELE = "gele"          # Freeze actif (classique seulement)


class GameScene(BaseScene):
    """Scène de jeu - mode classique et challenge."""
    
    # Taille de police pour le score
    SCORE_FONT_SIZE = 40
    
    # Paramètres de transition explosion
    FLASH_DURATION = 1.0
    FADE_TO_BLACK_DURATION = 0.5
    
    # Durées des états temporaires de Yoshi
    YOSHI_CONTENT_DURATION = 3.0  # secondes
    YOSHI_TRISTE_DURATION = 5.0   # secondes
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.font_score = None
        self.font_letter = None
        
        # Images HUD
        self.heart_full_img = None
        self.heart_empty_img = None
        self.gauge_img = None
        self.gauge_segments = []
        self.timer_frame_img = None
        
        # Images Yoshi
        self.yoshi_images = {}  # Dict[YoshiState, pygame.Surface]
        
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
        self.splashes: List[Splash] = []
        self.hearts = GameConfig.MAX_HEARTS
        self.game_time = 0.0
        self.is_frozen = False
        self.freeze_timer = 0.0
        self.game_over = False
        self.exploded = False
        
        # État de Yoshi
        self.yoshi_state = YoshiState.ATTEND
        self.yoshi_temp_timer = 0.0  # Timer pour les états temporaires
        
        # Système de transition explosion
        self.transition_state = 'playing'
        self.transition_timer = 0.0
        self.white_overlay = None
        self.black_overlay = None
        
        # Accumulation des fruits tranchés pendant un tracé souris
        self._stroke_sliced_fruits: List[Fruit] = []
        self._was_slicing = False
        
        # Mode de jeu
        self.mode = 'classic'
        self.difficulty = 'normal'
        self.challenge_timer = 0.0
        
        # Tracking audio pour les bombes
        self._bomb_count = 0
    
    def setup(self):
        """Initialise la partie."""
        self.mode = self.scene_manager.shared_data.get('mode', 'classic')
        self.difficulty = self.scene_manager.shared_data.get('difficulty', 'normal')
        control_mode = self.scene_manager.shared_data.get('control_mode', 'keyboard')
        
        self._load_resources()
        
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
        
        # Reset Yoshi
        self.yoshi_state = YoshiState.ATTEND
        self.yoshi_temp_timer = 0.0
        
        # Reset transition
        self.transition_state = 'playing'
        self.transition_timer = 0.0
        
        # Reset audio
        self._bomb_count = 0
        audio_manager.stop_bomb_alert()
        
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
        self.font_letter = pygame.font.Font(font_path, 72)
        
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
        
        # Timer (challenge)
        if self.mode == 'challenge':
            self.timer_frame_img = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.CHALLENGE_TIMER_FRAME)
            ).convert_alpha()
        
        # Boutons
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
        
        # Overlays pour transitions
        self.white_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.white_overlay.fill((255, 255, 255))
        self.black_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.black_overlay.fill((0, 0, 0))
        
        # Charger les images de Yoshi selon le mode
        self._load_yoshi_images()
    
    def _load_yoshi_images(self):
        """Charge les images de Yoshi selon le mode de jeu."""
        self.yoshi_images = {}
        
        if self.mode == 'challenge':
            # Mode Challenge : attend, content, triste seulement
            self.yoshi_images[YoshiState.ATTEND] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CHALLENGE_ATTEND)
            ).convert_alpha()
            self.yoshi_images[YoshiState.CONTENT] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CHALLENGE_CONTENT)
            ).convert_alpha()
            self.yoshi_images[YoshiState.TRISTE] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CHALLENGE_TRISTE)
            ).convert_alpha()
        else:
            # Mode Classique : tous les états
            self.yoshi_images[YoshiState.ATTEND] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CLASSIC_ATTEND)
            ).convert_alpha()
            self.yoshi_images[YoshiState.CONTENT] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CLASSIC_CONTENT)
            ).convert_alpha()
            self.yoshi_images[YoshiState.TRISTE] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CLASSIC_TRISTE)
            ).convert_alpha()
            self.yoshi_images[YoshiState.GELE] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CLASSIC_GELE)
            ).convert_alpha()
            self.yoshi_images[YoshiState.AFFAME] = pygame.image.load(
                os.path.join(IMAGES_DIR, Images.YOSHI_CLASSIC_AFFAME)
            ).convert_alpha()
    
    def set_achievement_manager(self, manager: AchievementManager):
        """Définit le gestionnaire de succès."""
        self.achievement_manager = manager
    
    # ==================== SYSTÈME D'ÉTATS YOSHI ====================
    
    def _set_yoshi_state(self, state: YoshiState, temporary: bool = False, duration: float = 0.0):
        """
        Change l'état de Yoshi.
        
        Args:
            state: Nouvel état
            temporary: Si True, l'état reviendra à ATTEND après duration
            duration: Durée de l'état temporaire
        """
        self.yoshi_state = state
        if temporary:
            self.yoshi_temp_timer = duration
        else:
            self.yoshi_temp_timer = 0.0
    
    def _get_current_yoshi_state(self) -> YoshiState:
        """
        Retourne l'état actuel de Yoshi selon la priorité.
        
        Priorité (plus haute → plus basse) :
        1. Gelé (freeze actif) - classique seulement
        2. Affamé (1 cœur restant) - classique seulement
        3. Triste (temporaire)
        4. Content (temporaire)
        5. Attend (défaut)
        """
        # En mode classique, vérifier les états prioritaires permanents
        if self.mode == 'classic':
            # Priorité 1 : Gelé
            if self.is_frozen:
                return YoshiState.GELE
            
            # Priorité 2 : Affamé (1 cœur restant)
            if self.hearts == 1:
                return YoshiState.AFFAME
        
        # Les états temporaires (triste, content) sont gérés par yoshi_state
        # et le timer gère leur expiration
        return self.yoshi_state
    
    def _update_yoshi_state(self, dt: float):
        """Met à jour l'état temporaire de Yoshi."""
        if self.yoshi_temp_timer > 0:
            self.yoshi_temp_timer -= dt
            if self.yoshi_temp_timer <= 0:
                # L'état temporaire expire, revenir à ATTEND
                self.yoshi_state = YoshiState.ATTEND
                self.yoshi_temp_timer = 0.0
    
    def _on_combo(self, count: int):
        """Appelé quand un combo est réalisé (3+ fruits)."""
        if count >= 3:
            self._set_yoshi_state(YoshiState.CONTENT, temporary=True, duration=self.YOSHI_CONTENT_DURATION)
    
    def _on_heart_lost_yoshi(self):
        """Appelé quand un cœur est perdu - met Yoshi triste temporairement."""
        # Triste seulement si on a encore des cœurs (sinon game over)
        if self.hearts > 0:
            self._set_yoshi_state(YoshiState.TRISTE, temporary=True, duration=self.YOSHI_TRISTE_DURATION)
    
    def _on_bomb_penalty_yoshi(self):
        """Appelé en mode challenge quand une bombe est tranchée (-10 pts)."""
        self._set_yoshi_state(YoshiState.TRISTE, temporary=True, duration=self.YOSHI_TRISTE_DURATION)
    
    # ==================== CALLBACKS BOUTONS ====================
    
    def _on_settings(self):
        pass
    
    def _on_quit(self):
        audio_manager.stop_bomb_alert()
        self.scene_manager.change_scene('menu')
    
    # ==================== ÉVÉNEMENTS ====================
    
    def handle_events(self, events: List[pygame.event.Event]):
        if self.game_over or self.transition_state != 'playing':
            return
        
        for event in events:
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            self.input_handler.handle_event(event)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._on_quit()
    
    # ==================== UPDATE ====================
    
    def update(self, dt: float):
        if self.transition_state != 'playing':
            self._update_transition(dt)
            return
        
        if self.game_over:
            return
        
        self.game_time += dt
        
        # Mode challenge : décompte
        if self.mode == 'challenge':
            self.challenge_timer -= dt
            if self.challenge_timer <= 0:
                self._end_game()
                return
        
        # Freeze
        if self.is_frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self._unfreeze_all()
        
        # Multiplicateur
        self.scoring.update(dt)
        
        # Spawn
        if not self.is_frozen:
            keyboard_mode = self.input_handler.mode == "keyboard"
            new_entities = self.spawner.update(dt, keyboard_mode)
            
            for entity in new_entities:
                if isinstance(entity, Bomb):
                    self._on_bomb_spawned()
            
            self.entities.extend(new_entities)
        
        # Entités
        for entity in self.entities:
            entity.update(dt)
        
        # Éclaboussures
        for splash in self.splashes:
            splash.update(dt)
        
        # Détection tranches
        sliced = self.input_handler.get_sliced_entities(self.entities)
        if sliced:
            self._process_sliced(sliced)
        
        # Fin de tracé souris
        is_slicing = self.input_handler.is_slicing()
        if self._was_slicing and not is_slicing:
            self._finalize_stroke()
        self._was_slicing = is_slicing
        
        # Vérifications
        self._check_freeze_end()
        self._check_missed_entities()
        self._cleanup_entities()
        self.splashes = [s for s in self.splashes if not s.finished]
        
        # Mise à jour état Yoshi
        self._update_yoshi_state(dt)
        
        # Succès
        if self.achievement_manager:
            self.achievement_manager.on_time_update(self.game_time)
    
    def _update_transition(self, dt: float):
        """Met à jour la transition d'explosion."""
        self.transition_timer += dt
        
        if self.transition_state == 'flash':
            if self.transition_timer >= self.FLASH_DURATION:
                self.transition_state = 'fade_to_black'
                self.transition_timer = 0.0
        
        elif self.transition_state == 'fade_to_black':
            if self.transition_timer >= self.FADE_TO_BLACK_DURATION:
                self.transition_state = 'finished'
                self._finalize_game_over()
    
    def _start_explosion_transition(self):
        """Démarre la transition d'explosion."""
        self.transition_state = 'flash'
        self.transition_timer = 0.0
        self.exploded = True
        self.game_over = True
        
        audio_manager.stop_bomb_alert()
        audio_manager.play_sfx('game_over')
        
        if self.achievement_manager:
            self.achievement_manager.end_game(self.exploded)
    
    def _finalize_game_over(self):
        """Appelé quand la transition est terminée."""
        self.scene_manager.shared_data['last_score'] = self.scoring.score
        self.scene_manager.shared_data['exploded'] = self.exploded
        self.scene_manager.change_scene('game_over')
    
    def _finalize_stroke(self):
        """Finalise un tracé souris."""
        if not self._stroke_sliced_fruits:
            return
        
        fruits = self._stroke_sliced_fruits
        count = len(fruits)
        
        points = self.scoring.add_sliced_fruits(count)
        
        # Combo
        if count >= 3:
            self._on_combo(count)
        
        # Jauge bonus
        fruit_types = [f.fruit_type for f in fruits]
        for fruit_type in set(fruit_types):
            if fruit_types.count(fruit_type) >= 2:
                if self.bonus_gauge.add_cran():
                    self._activate_multiplier()
        
        if self.achievement_manager:
            self.achievement_manager.on_fruit_sliced(count)
            self.achievement_manager.on_score_update(self.scoring.score)
        
        self._stroke_sliced_fruits.clear()
    
    def _process_sliced(self, sliced: List[Entity]):
        """Traite les entités tranchées."""
        fruits_sliced = []
        bomb_sliced = False
        ice_sliced = False
        
        for entity in sliced:
            entity.slice()
            
            if entity.letter:
                self.spawner.release_letter(entity.letter)
            
            if isinstance(entity, Fruit):
                fruits_sliced.append(entity)
            elif isinstance(entity, Bomb):
                bomb_sliced = True
                self._on_bomb_removed()
            elif isinstance(entity, Ice):
                ice_sliced = True
        
        if bomb_sliced:
            self._on_bomb_sliced()
            return
        
        if ice_sliced:
            self._on_ice_sliced()
        
        if fruits_sliced:
            self._on_fruits_sliced(fruits_sliced)
    
    def _on_fruits_sliced(self, fruits: List[Fruit]):
        """Appelé quand des fruits sont tranchés."""
        for fruit in fruits:
            cx, cy = fruit.center
            splash = Splash(fruit.fruit_type, cx, cy)
            self.splashes.append(splash)
        
        if self.input_handler.mode == "mouse":
            self._stroke_sliced_fruits.extend(fruits)
        else:
            count = len(fruits)
            self.scoring.add_sliced_fruits(count)
            
            if count >= 3:
                self._on_combo(count)
            
            fruit_types = [f.fruit_type for f in fruits]
            for fruit_type in set(fruit_types):
                if fruit_types.count(fruit_type) >= 2:
                    if self.bonus_gauge.add_cran():
                        self._activate_multiplier()
            
            if self.achievement_manager:
                self.achievement_manager.on_fruit_sliced(count)
                self.achievement_manager.on_score_update(self.scoring.score)
    
    def _on_bomb_sliced(self):
        """Appelé quand une bombe est tranchée."""
        if self.mode == 'challenge':
            penalty = DIFFICULTY['challenge']['bomb_penalty']
            self.scoring.apply_bomb_penalty(penalty)
            self._on_bomb_penalty_yoshi()  # Yoshi triste
        else:
            self._start_explosion_transition()
    
    def _on_ice_sliced(self):
        """Appelé quand un glaçon est tranché."""
        if self.mode == 'challenge':
            return
        
        audio_manager.play_sfx('freeze')
        
        freeze_duration = DIFFICULTY.get(self.difficulty, DIFFICULTY['normal']).get('freeze_duration', 4.0)
        self._freeze_all(freeze_duration)
        
        if self.achievement_manager:
            self.achievement_manager.on_ice_sliced()
    
    def _freeze_all(self, duration: float):
        """Gèle tous les fruits."""
        self.is_frozen = True
        self.freeze_timer = duration
        
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
        """Vérifie si le freeze doit se terminer."""
        if not self.is_frozen:
            return
        
        frozen_fruits = [
            e for e in self.entities 
            if isinstance(e, Fruit) and e.frozen and not e.sliced
        ]
        
        if len(frozen_fruits) == 0:
            self._unfreeze_all()
    
    def _activate_multiplier(self):
        """Active le multiplicateur."""
        if self.scoring.has_multiplier:
            self.scoring.increase_multiplier(
                BonusGauge.MULTIPLIER_INCREMENT,
                BonusGauge.MULTIPLIER_DURATION
            )
        else:
            self.scoring.activate_multiplier(2, BonusGauge.MULTIPLIER_DURATION)
    
    def _check_missed_entities(self):
        """Vérifie les entités sorties de l'écran."""
        for entity in self.entities:
            if entity.sliced or entity.missed:
                continue
            
            if entity.y > GameConfig.GAME_ZONE_BOTTOM:
                entity.missed = True
                
                if isinstance(entity, Fruit):
                    self._on_fruit_missed()
                elif isinstance(entity, Bomb):
                    self._on_bomb_removed()
                    if self.achievement_manager:
                        self.achievement_manager.on_bomb_avoided()
    
    def _on_fruit_missed(self):
        """Appelé quand un fruit est raté."""
        if self.mode == 'challenge':
            return
        
        self.hearts -= 1
        
        # Yoshi triste
        self._on_heart_lost_yoshi()
        
        if self.achievement_manager:
            self.achievement_manager.on_heart_lost()
        
        if self.hearts <= 0:
            self._end_game()
    
    def _cleanup_entities(self):
        """Supprime les entités sorties."""
        self.entities = [
            e for e in self.entities
            if not (e.missed or e.y > GameConfig.GAME_ZONE_BOTTOM)
        ]
    
    # ==================== AUDIO BOMBES ====================
    
    def _on_bomb_spawned(self):
        """Appelé quand une bombe apparaît."""
        self._bomb_count += 1
        if self._bomb_count == 1:
            audio_manager.start_bomb_alert()
    
    def _on_bomb_removed(self):
        """Appelé quand une bombe disparaît."""
        self._bomb_count = max(0, self._bomb_count - 1)
        if self._bomb_count == 0:
            audio_manager.stop_bomb_alert()
    
    # ==================== FIN DE PARTIE ====================
    
    def _end_game(self):
        """Termine la partie."""
        self.game_over = True
        
        audio_manager.stop_bomb_alert()
        audio_manager.play_sfx('game_over')
        
        if self.achievement_manager:
            self.achievement_manager.end_game(self.exploded)
        
        self.scene_manager.shared_data['last_score'] = self.scoring.score
        self.scene_manager.shared_data['exploded'] = self.exploded
        
        self.scene_manager.change_scene('game_over')
    
    # ==================== RENDU ====================
    
    def render(self, screen: pygame.Surface):
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Yoshi (dans la zone de décor, pas clippé)
        self._render_yoshi(screen)
        
        # Zone de jeu clippée
        game_zone_rect = pygame.Rect(
            GameConfig.GAME_ZONE_LEFT,
            GameConfig.GAME_ZONE_TOP,
            GameConfig.GAME_ZONE_SIZE[0],
            GameConfig.GAME_ZONE_SIZE[1]
        )
        screen.set_clip(game_zone_rect)
        
        # Éclaboussures
        for splash in self.splashes:
            splash.render(screen)
        
        # Entités
        for entity in self.entities:
            entity.render(screen, self.font_letter if self.input_handler.mode == "keyboard" else None)
        
        # Traînée souris
        if self.input_handler.mode == "mouse" and self.input_handler.is_slicing():
            self._render_trail(screen)
        
        screen.set_clip(None)
        
        # HUD
        self._render_hud(screen)
        
        # Transition
        self._render_transition(screen)
    
    def _render_yoshi(self, screen: pygame.Surface):
        """Affiche Yoshi avec son état actuel."""
        current_state = self._get_current_yoshi_state()
        
        # Récupérer l'image correspondante
        yoshi_img = self.yoshi_images.get(current_state)
        
        if yoshi_img:
            yoshi_rect = yoshi_img.get_rect(center=Layout.GAME_YOSHI)
            screen.blit(yoshi_img, yoshi_rect)
    
    def _render_transition(self, screen: pygame.Surface):
        """Affiche les effets de transition."""
        if self.transition_state == 'flash':
            progress = self.transition_timer / self.FLASH_DURATION
            alpha = int(255 * (1 - progress * 0.3))
            self.white_overlay.set_alpha(alpha)
            screen.blit(self.white_overlay, (0, 0))
        
        elif self.transition_state == 'fade_to_black':
            progress = self.transition_timer / self.FADE_TO_BLACK_DURATION
            alpha = int(255 * progress)
            self.black_overlay.set_alpha(alpha)
            screen.blit(self.black_overlay, (0, 0))
    
    def _render_trail(self, screen: pygame.Surface):
        """Affiche la traînée de la souris."""
        points = self.input_handler.get_trail_points()
        if len(points) < 2:
            return
        
        for i in range(1, len(points)):
            color = (255, 255, 255)
            pygame.draw.line(screen, color, points[i-1], points[i], 3)
    
    def _render_hud(self, screen: pygame.Surface):
        """Affiche le HUD."""
        self._render_score(screen)
        
        if self.mode == 'challenge':
            self._render_timer(screen)
        else:
            self._render_hearts(screen)
        
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
        
        self._render_gauge(screen)
    
    def _render_score(self, screen: pygame.Surface):
        """Affiche le score."""
        score_text = f"{self.scoring.score}"
        
        if self.scoring.has_multiplier:
            score_text += f" x{self.scoring.multiplier}"
            timer_left = int(self.scoring.multiplier_timer)
            score_text += f" ({timer_left}s)"
        
        score_surface = self.font_score.render(score_text, True, TextColors.GAME_SCORE)
        score_rect = score_surface.get_rect(left=Layout.GAME_SCORE_POS_CLASSIC[0], centery=Layout.GAME_SCORE_POS_CLASSIC[1])
        screen.blit(score_surface, score_rect)
    
    def _render_hearts(self, screen: pygame.Surface):
        """Affiche les 3 cœurs."""
        heart_positions = [
            Layout.GAME_HEART_1,
            Layout.GAME_HEART_2,
            Layout.GAME_HEART_3,
        ]
        
        for i, pos in enumerate(heart_positions):
            img = self.heart_full_img if i < self.hearts else self.heart_empty_img
            rect = img.get_rect(center=pos)
            screen.blit(img, rect)
    
    def _render_timer(self, screen: pygame.Surface):
        """Affiche le timer."""
        if self.timer_frame_img:
            frame_rect = self.timer_frame_img.get_rect(center=Layout.GAME_TIMER)
            screen.blit(self.timer_frame_img, frame_rect)
        
        minutes = int(self.challenge_timer) // 60
        seconds = int(self.challenge_timer) % 60
        timer_text = f"{minutes}:{seconds:02d}"
        
        timer_surface = self.font_score.render(timer_text, True, TextColors.GAME_SCORE)
        timer_rect = timer_surface.get_rect(center=Layout.GAME_TIMER)
        screen.blit(timer_surface, timer_rect)
    
    def _render_gauge(self, screen: pygame.Surface):
        """Affiche la jauge de bonus."""
        gauge_rect = self.gauge_img.get_rect(center=Layout.GAME_GAUGE)
        screen.blit(self.gauge_img, gauge_rect)
        
        crans = self.bonus_gauge.crans
        for i in range(crans):
            if i < len(self.gauge_segments):
                segment_img = self.gauge_segments[i]
                segment_pos = Layout.GAME_GAUGE_SEGMENTS[i]
                segment_rect = segment_img.get_rect(center=segment_pos)
                screen.blit(segment_img, segment_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie."""
        audio_manager.stop_bomb_alert()
        self.entities.clear()
        if self.input_handler:
            self.input_handler.reset()
