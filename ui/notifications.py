"""
NotificationManager - Gestionnaire des notifications de succès
Jour 3 - Dev 3

Affiche les notifications quand un succès est débloqué :
- Animation d'apparition/disparition
- Icône étoile dorée style Mario
- Son de célébration (1-UP)
"""

import pygame
import math
from typing import List, Optional
from dataclasses import dataclass
from core.achievements import Achievement


# Couleurs thème Mario/Yoshi
COLORS = {
    'background': (50, 50, 50, 230),    # Fond semi-transparent
    'border': (255, 193, 7),            # Or étoile #FFC107
    'title': (255, 213, 79),            # Jaune pièces #FFD54F
    'description': (255, 255, 255),     # Blanc
    'star': (255, 193, 7),              # Or étoile
}


@dataclass
class NotificationItem:
    """Représente une notification en cours d'affichage"""
    achievement: Achievement
    time_remaining: float
    animation_phase: str  # 'enter', 'display', 'exit'
    animation_progress: float  # 0.0 à 1.0
    y_offset: int  # Position verticale (pour empiler)


class NotificationManager:
    """
    Gestionnaire des notifications de succès.
    Affiche les succès débloqués avec une animation style Nintendo.
    """
    
    # Configuration
    NOTIFICATION_DURATION = 3.0  # Durée d'affichage en secondes
    ENTER_DURATION = 0.3        # Durée de l'animation d'entrée
    EXIT_DURATION = 0.3         # Durée de l'animation de sortie
    
    NOTIFICATION_WIDTH = 350
    NOTIFICATION_HEIGHT = 80
    NOTIFICATION_MARGIN = 10
    
    MAX_NOTIFICATIONS = 3       # Nombre max de notifications simultanées
    
    def __init__(self):
        self.notifications: List[NotificationItem] = []
        self.pending_achievements: List[Achievement] = []
        
        # Fonts (initialisées au premier render)
        self.font_title: Optional[pygame.font.Font] = None
        self.font_desc: Optional[pygame.font.Font] = None
        self.fonts_initialized = False
        
        # Son (à charger par le jeu)
        self.sound_achievement: Optional[pygame.mixer.Sound] = None
    
    def set_achievement_sound(self, sound: pygame.mixer.Sound):
        """Définit le son à jouer lors d'un succès"""
        self.sound_achievement = sound
    
    def add_notification(self, achievement: Achievement):
        """
        Ajoute une notification à afficher.
        
        Args:
            achievement: Le succès débloqué à afficher
        """
        self.pending_achievements.append(achievement)
    
    def add_notifications(self, achievements: List[Achievement]):
        """
        Ajoute plusieurs notifications à afficher.
        
        Args:
            achievements: Liste des succès débloqués
        """
        self.pending_achievements.extend(achievements)
    
    def _init_fonts(self):
        """Initialise les fonts si ce n'est pas déjà fait"""
        if not self.fonts_initialized:
            pygame.font.init()
            self.font_title = pygame.font.Font(None, 28)
            self.font_desc = pygame.font.Font(None, 20)
            self.fonts_initialized = True
    
    def update(self, dt: float):
        """
        Met à jour les notifications.
        
        Args:
            dt: Temps écoulé depuis la dernière frame (en secondes)
        """
        # Ajouter les notifications en attente
        while self.pending_achievements and len(self.notifications) < self.MAX_NOTIFICATIONS:
            achievement = self.pending_achievements.pop(0)
            y_offset = len(self.notifications) * (self.NOTIFICATION_HEIGHT + self.NOTIFICATION_MARGIN)
            
            notification = NotificationItem(
                achievement=achievement,
                time_remaining=self.NOTIFICATION_DURATION,
                animation_phase='enter',
                animation_progress=0.0,
                y_offset=y_offset
            )
            self.notifications.append(notification)
            
            # Jouer le son
            if self.sound_achievement:
                self.sound_achievement.play()
        
        # Mettre à jour les notifications actives
        notifications_to_remove = []
        
        for notification in self.notifications:
            if notification.animation_phase == 'enter':
                # Animation d'entrée
                notification.animation_progress += dt / self.ENTER_DURATION
                if notification.animation_progress >= 1.0:
                    notification.animation_progress = 1.0
                    notification.animation_phase = 'display'
            
            elif notification.animation_phase == 'display':
                # Affichage normal
                notification.time_remaining -= dt
                if notification.time_remaining <= 0:
                    notification.animation_phase = 'exit'
                    notification.animation_progress = 0.0
            
            elif notification.animation_phase == 'exit':
                # Animation de sortie
                notification.animation_progress += dt / self.EXIT_DURATION
                if notification.animation_progress >= 1.0:
                    notifications_to_remove.append(notification)
        
        # Supprimer les notifications terminées
        for notification in notifications_to_remove:
            self.notifications.remove(notification)
        
        # Réorganiser les positions Y
        for i, notification in enumerate(self.notifications):
            target_y = i * (self.NOTIFICATION_HEIGHT + self.NOTIFICATION_MARGIN)
            # Animation douce vers la position cible
            notification.y_offset += (target_y - notification.y_offset) * min(1.0, dt * 10)
    
    def render(self, screen: pygame.Surface):
        """
        Affiche les notifications.
        
        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        self._init_fonts()
        
        screen_width = screen.get_width()
        
        for notification in self.notifications:
            self._render_notification(screen, notification, screen_width)
    
    def _render_notification(self, screen: pygame.Surface, notification: NotificationItem, screen_width: int):
        """Affiche une notification individuelle"""
        # Calculer la position X avec animation
        target_x = screen_width - self.NOTIFICATION_WIDTH - 20
        
        if notification.animation_phase == 'enter':
            # Slide depuis la droite
            progress = self._ease_out_cubic(notification.animation_progress)
            x = screen_width + (target_x - screen_width) * progress
        elif notification.animation_phase == 'exit':
            # Slide vers la droite
            progress = self._ease_in_cubic(notification.animation_progress)
            x = target_x + (screen_width - target_x) * progress
        else:
            x = target_x
        
        y = 20 + notification.y_offset
        
        # Créer une surface avec transparence
        notification_surface = pygame.Surface(
            (self.NOTIFICATION_WIDTH, self.NOTIFICATION_HEIGHT),
            pygame.SRCALPHA
        )
        
        # Fond arrondi
        pygame.draw.rect(
            notification_surface,
            COLORS['background'],
            (0, 0, self.NOTIFICATION_WIDTH, self.NOTIFICATION_HEIGHT),
            border_radius=10
        )
        
        # Bordure dorée
        pygame.draw.rect(
            notification_surface,
            COLORS['border'],
            (0, 0, self.NOTIFICATION_WIDTH, self.NOTIFICATION_HEIGHT),
            3,
            border_radius=10
        )
        
        # Étoile animée
        star_x = 40
        star_y = self.NOTIFICATION_HEIGHT // 2
        star_size = 20
        
        # Animation de pulsation de l'étoile
        if notification.animation_phase == 'display':
            pulse = 1.0 + 0.1 * math.sin(notification.time_remaining * 8)
            star_size = int(20 * pulse)
        
        self._draw_star(notification_surface, star_x, star_y, star_size, COLORS['star'])
        
        # Texte "Succès débloqué !"
        header_text = self.font_desc.render("★ Succès débloqué !", True, COLORS['title'])
        notification_surface.blit(header_text, (70, 12))
        
        # Nom du succès
        name_text = self.font_title.render(notification.achievement.name, True, COLORS['description'])
        # Tronquer si trop long
        max_width = self.NOTIFICATION_WIDTH - 90
        if name_text.get_width() > max_width:
            name = notification.achievement.name
            while name_text.get_width() > max_width and len(name) > 3:
                name = name[:-4] + "..."
                name_text = self.font_title.render(name, True, COLORS['description'])
        notification_surface.blit(name_text, (70, 32))
        
        # Description courte
        desc_text = self.font_desc.render(notification.achievement.description[:50], True, COLORS['description'])
        if len(notification.achievement.description) > 50:
            desc = notification.achievement.description[:47] + "..."
            desc_text = self.font_desc.render(desc, True, COLORS['description'])
        notification_surface.blit(desc_text, (70, 55))
        
        # Dessiner sur l'écran principal
        screen.blit(notification_surface, (int(x), int(y)))
    
    def _draw_star(self, surface: pygame.Surface, cx: int, cy: int, size: int, color):
        """Dessine une étoile à 5 branches"""
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.4
            px = cx + r * math.cos(angle)
            py = cy - r * math.sin(angle)
            points.append((px, py))
        
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 2)
    
    def _ease_out_cubic(self, t: float) -> float:
        """Fonction d'easing pour animation fluide (sortie)"""
        return 1 - pow(1 - t, 3)
    
    def _ease_in_cubic(self, t: float) -> float:
        """Fonction d'easing pour animation fluide (entrée)"""
        return t * t * t
    
    def has_notifications(self) -> bool:
        """Retourne True s'il y a des notifications actives ou en attente"""
        return len(self.notifications) > 0 or len(self.pending_achievements) > 0
    
    def clear_all(self):
        """Supprime toutes les notifications"""
        self.notifications.clear()
        self.pending_achievements.clear()


# ==================== EXEMPLE D'UTILISATION ====================

if __name__ == "__main__":
    """Test du système de notifications"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Notifications")
    clock = pygame.time.Clock()
    
    # Créer le manager
    notification_manager = NotificationManager()
    
    # Créer des succès de test
    test_achievements = [
        Achievement(
            id="test1",
            name="Premier Repas",
            description="Yoshi a goûté à ses premiers fruits !",
            category="fruits_total",
            condition_type="total_fruits_gte",
            condition_value=10,
            unlocked=True
        ),
        Achievement(
            id="test2",
            name="Langue Agile",
            description="Yoshi attrape plusieurs fruits d'un coup !",
            category="combos",
            condition_type="combo_gte",
            condition_value=3,
            unlocked=True
        ),
        Achievement(
            id="test3",
            name="Bébé Yoshi",
            description="Premiers pas dans l'aventure !",
            category="score_partie",
            condition_type="score_gte",
            condition_value=10,
            unlocked=True
        ),
    ]
    
    # Ajouter les notifications avec délai
    notification_manager.add_notification(test_achievements[0])
    
    running = True
    timer = 0
    achievement_index = 1
    
    while running:
        dt = clock.tick(60) / 1000.0
        timer += dt
        
        # Ajouter une nouvelle notification toutes les 2 secondes
        if timer > 2.0 and achievement_index < len(test_achievements):
            notification_manager.add_notification(test_achievements[achievement_index])
            achievement_index += 1
            timer = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and achievement_index < len(test_achievements):
                    notification_manager.add_notification(test_achievements[achievement_index])
                    achievement_index += 1
        
        # Mise à jour
        notification_manager.update(dt)
        
        # Rendu
        screen.fill((129, 212, 250))  # Bleu ciel
        notification_manager.render(screen)
        
        # Instructions
        font = pygame.font.Font(None, 30)
        text = font.render("Appuyez sur ESPACE pour ajouter une notification", True, (0, 0, 0))
        screen.blit(text, (200, 300))
        
        pygame.display.flip()
    
    pygame.quit()
