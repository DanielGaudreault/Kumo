import pygame
import sys
import math
import random
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kumo - Your Emotional Companion Robot")

# Colors
BACKGROUND = (25, 25, 40)
ROBOT_BASE = (80, 90, 130)
ROBOT_HIGHLIGHT = (120, 140, 200)
HAPPY_COLOR = (255, 220, 100)
SAD_COLOR = (100, 150, 255)
CALM_COLOR = (180, 220, 180)
EXCITED_COLOR = (255, 150, 150)
NEUTRAL_COLOR = (200, 200, 220)
TOUCH_COLOR = (250, 200, 200)

# Robot states
class RobotState:
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    CALM = 3
    EXCITED = 4

# Main robot class
class EmotionalRobot:
    def __init__(self):
        self.state = RobotState.NEUTRAL
        self.position = (WIDTH // 2, HEIGHT // 2)
        self.size = 120
        self.pulse_value = 0
        self.pulse_direction = 1
        self.touch_timer = 0
        self.interaction_level = 50
        self.mood_timer = 0
        self.current_mood = RobotState.NEUTRAL
        self.messages = [
            "I'm here for you",
            "You're doing great",
            "Take a deep breath",
            "I'm listening",
            "You matter"
        ]
        self.current_message = ""
        self.message_timer = 0
        
    def update(self):
        # Update pulse animation
        self.pulse_value += 0.05 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_value = 1.0
            self.pulse_direction = -1
        elif self.pulse_value <= 0.0:
            self.pulse_value = 0.0
            self.pulse_direction = 1
            
        # Update touch timer
        if self.touch_timer > 0:
            self.touch_timer -= 1
            
        # Update mood
        self.mood_timer -= 1
        if self.mood_timer <= 0:
            self.change_mood()
            
        # Update message
        self.message_timer -= 1
        if self.message_timer <= 0:
            self.current_message = ""
        
    def draw(self, surface):
        # Draw base (cloud-like shape)
        self.draw_cloud(surface, self.position, self.size)
        
        # Draw face based on state
        self.draw_face(surface)
        
        # Draw touch effect if active
        if self.touch_timer > 0:
            self.draw_touch_effect(surface)
            
        # Draw message if any
        if self.current_message:
            self.draw_message(surface)
            
        # Draw status info
        self.draw_status(surface)
    
    def draw_cloud(self, surface, pos, size):
        # Draw a soft cloud-like shape
        x, y = pos
        
        # Base circle
        pygame.draw.circle(surface, ROBOT_BASE, (x, y), size)
        
        # Additional circles for cloud effect
        pygame.draw.circle(surface, ROBOT_BASE, (x - size//2, y), size//1.5)
        pygame.draw.circle(surface, ROBOT_BASE, (x + size//2, y), size//1.5)
        pygame.draw.circle(surface, ROBOT_BASE, (x, y - size//2), size//1.8)
        pygame.draw.circle(surface, ROBOT_BASE, (x, y + size//3), size//1.8)
        
        # Add highlight
        highlight_pos = (x - size//3, y - size//3)
        pygame.draw.circle(surface, ROBOT_HIGHLIGHT, highlight_pos, size//3, 3)
        
    def draw_face(self, surface):
        x, y = self.position
        
        # Draw eyes
        eye_spacing = self.size // 3
        eye_y = y - self.size // 10
        eye_radius = self.size // 8
        
        # Draw eyes based on mood
        if self.state == RobotState.HAPPY:
            # Happy eyes
            pygame.draw.circle(surface, (30, 30, 40), (x - eye_spacing, eye_y), eye_radius)
            pygame.draw.circle(surface, (30, 30, 40), (x + eye_spacing, eye_y), eye_radius)
            
            # Happy mouth
            mouth_start = (x - self.size//3, y + self.size//4)
            mouth_end = (x + self.size//3, y + self.size//4)
            control = (x, y + self.size//2)
            
            pygame.draw.arc(surface, (30, 30, 40), 
                           (mouth_start[0], mouth_start[1], self.size//1.5, self.size//3),
                           math.pi, 2*math.pi, 3)
            
        elif self.state == RobotState.SAD:
            # Sad eyes
            pygame.draw.circle(surface, (30, 30, 40), (x - eye_spacing, eye_y), eye_radius)
            pygame.draw.circle(surface, (30, 30, 40), (x + eye_spacing, eye_y), eye_radius)
            
            # Sad mouth
            mouth_start = (x - self.size//3, y + self.size//2)
            mouth_end = (x + self.size//3, y + self.size//2)
            
            pygame.draw.arc(surface, (30, 30, 40), 
                           (mouth_start[0], mouth_start[1] - self.size//4, self.size//1.5, self.size//3),
                           0, math.pi, 3)
            
        elif self.state == RobotState.CALM:
            # Calm eyes (closed)
            pygame.draw.line(surface, (30, 30, 40), (x - eye_spacing - eye_radius, eye_y), 
                            (x - eye_spacing + eye_radius, eye_y), 2)
            pygame.draw.line(surface, (30, 30, 40), (x + eye_spacing - eye_radius, eye_y), 
                            (x + eye_spacing + eye_radius, eye_y), 2)
            
            # Calm mouth (straight)
            pygame.draw.line(surface, (30, 30, 40), 
                            (x - self.size//4, y + self.size//3),
                            (x + self.size//4, y + self.size//3), 2)
            
        elif self.state == RobotState.EXCITED:
            # Excited eyes (sparkling)
            pygame.draw.circle(surface, (30, 30, 40), (x - eye_spacing, eye_y), eye_radius)
            pygame.draw.circle(surface, (30, 30, 40), (x + eye_spacing, eye_y), eye_radius)
            
            # Draw sparkle lines
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                end_x = (x - eye_spacing) + math.cos(rad) * (eye_radius + 5)
                end_y = eye_y + math.sin(rad) * (eye_radius + 5)
                pygame.draw.line(surface, (30, 30, 40), 
                                (x - eye_spacing, eye_y), (end_x, end_y), 2)
                
                end_x = (x + eye_spacing) + math.cos(rad) * (eye_radius + 5)
                end_y = eye_y + math.sin(rad) * (eye_radius + 5)
                pygame.draw.line(surface, (30, 30, 40), 
                                (x + eye_spacing, eye_y), (end_x, end_y), 2)
            
            # Excited mouth (open)
            pygame.draw.circle(surface, (30, 30, 40), (x, y + self.size//3), self.size//6)
            
        else:  # NEUTRAL
            # Neutral eyes
            pygame.draw.circle(surface, (30, 30, 40), (x - eye_spacing, eye_y), eye_radius)
            pygame.draw.circle(surface, (30, 30, 40), (x + eye_spacing, eye_y), eye_radius)
            
            # Neutral mouth
            pygame.draw.line(surface, (30, 30, 40), 
                            (x - self.size//4, y + self.size//3),
                            (x + self.size//4, y + self.size//3), 2)
        
        # Draw glow based on state
        glow_color = NEUTRAL_COLOR
        if self.state == RobotState.HAPPY:
            glow_color = HAPPY_COLOR
        elif self.state == RobotState.SAD:
            glow_color = SAD_COLOR
        elif self.state == RobotState.CALM:
            glow_color = CALM_COLOR
        elif self.state == RobotState.EXCITED:
            glow_color = EXCITED_COLOR
            
        # Draw pulsing glow
        glow_radius = self.size + int(self.pulse_value * 15)
        for alpha in range(5, 30, 5):
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, alpha), (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surf, (x - glow_radius, y - glow_radius))
    
    def draw_touch_effect(self, surface):
        x, y = self.position
        radius = self.size + (30 - self.touch_timer)
        alpha = self.touch_timer * 5
        
        touch_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(touch_surf, (*TOUCH_COLOR, alpha), (radius, radius), radius)
        surface.blit(touch_surf, (x - radius, y - radius))
    
    def draw_message(self, surface):
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(self.current_message, True, (240, 240, 240))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - self.size - 50))
        
        # Draw speech bubble
        bubble_rect = text_rect.inflate(30, 20)
        pygame.draw.rect(surface, (40, 40, 60), bubble_rect, border_radius=15)
        pygame.draw.rect(surface, (200, 200, 220), bubble_rect, 2, border_radius=15)
        
        # Draw pointer to robot
        points = [
            (WIDTH // 2, bubble_rect.bottom),
            (WIDTH // 2 - 10, bubble_rect.bottom + 10),
            (WIDTH // 2 + 10, bubble_rect.bottom + 10)
        ]
        pygame.draw.polygon(surface, (40, 40, 60), points)
        pygame.draw.polygon(surface, (200, 200, 220), points, 2)
        
        surface.blit(text, text_rect)
    
    def draw_status(self, surface):
        font = pygame.font.SysFont("Arial", 16)
        
        # Draw mood text
        mood_text = "Mood: "
        if self.state == RobotState.HAPPY:
            mood_text += "Happy"
        elif self.state == RobotState.SAD:
            mood_text += "Contemplative"
        elif self.state == RobotState.CALM:
            mood_text += "Calm"
        elif self.state == RobotState.EXCITED:
            mood_text += "Excited"
        else:
            mood_text += "Neutral"
            
        text = font.render(mood_text, True, (200, 200, 220))
        surface.blit(text, (20, 20))
        
        # Draw interaction level
        text = font.render(f"Connection: {self.interaction_level}%", True, (200, 200, 220))
        surface.blit(text, (20, 50))
        
        # Draw instructions
        instructions = [
            "Click on Kumo to interact",
            "Press 1-5 to change mood",
            "Press SPACE for a message",
            "Press R to reset interaction"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (150, 150, 170))
            surface.blit(text, (WIDTH - text.get_width() - 20, 20 + i*25))
    
    def handle_click(self, pos):
        x, y = self.position
        distance = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
        
        if distance <= self.size:
            self.touch_timer = 30
            self.interaction_level = min(100, self.interaction_level + 5)
            
            # 20% chance to show a message when touched
            if random.random() < 0.2:
                self.show_message()
                
            return True
        return False
    
    def change_mood(self, new_state=None):
        if new_state is not None:
            self.state = new_state
        else:
            # Randomly change to a new state
            current = self.state
            while current == self.state:
                self.state = random.randint(0, 4)
                
        self.mood_timer = random.randint(300, 600)  # 5-10 seconds at 60 FPS
        
    def show_message(self, message=None):
        if message:
            self.current_message = message
        else:
            self.current_message = random.choice(self.messages)
        self.message_timer = 180  # 3 seconds at 60 FPS

# Create robot instance
robot = EmotionalRobot()

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                robot.handle_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                robot.change_mood(RobotState.NEUTRAL)
            elif event.key == pygame.K_2:
                robot.change_mood(RobotState.HAPPY)
            elif event.key == pygame.K_3:
                robot.change_mood(RobotState.SAD)
            elif event.key == pygame.K_4:
                robot.change_mood(RobotState.CALM)
            elif event.key == pygame.K_5:
                robot.change_mood(RobotState.EXCITED)
            elif event.key == pygame.K_SPACE:
                robot.show_message()
            elif event.key == pygame.K_r:
                robot.interaction_level = 50
    
    # Update robot
    robot.update()
    
    # Draw everything
    screen.fill(BACKGROUND)
    
    # Draw stars in background
    for i in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.random() * 2
        brightness = random.randint(100, 200)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    robot.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
