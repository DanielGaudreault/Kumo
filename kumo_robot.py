import pygame
import sys
import math
import random

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
BUTTON_COLOR = (70, 80, 120)
BUTTON_HOVER = (100, 110, 150)

# Robot states
class RobotState:
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    CALM = 3
    EXCITED = 4

# Button class for UI
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, (200, 200, 220), self.rect, 2, border_radius=15)
        
        font = pygame.font.SysFont("Arial", 20)
        text_surf = font.render(self.text, True, (220, 220, 240))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

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
            "You matter",
            "I appreciate you",
            "Let's take a moment",
            "You're not alone",
            "I'm glad you're here",
            "You're enough"
        ]
        self.current_message = ""
        self.message_timer = 0
        self.heart_particles = []
        self.streak = 0
        self.last_interaction_time = pygame.time.get_ticks()
        
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
            
        # Update heart particles
        for i, particle in enumerate(self.heart_particles):
            particle[0] += particle[3]  # x += dx
            particle[1] += particle[4]  # y += dy
            particle[2] -= 0.05  # size decrease
            if particle[2] <= 0:
                self.heart_particles.pop(i)
                
        # Check if robot needs attention
        current_time = pygame.time.get_ticks()
        if current_time - self.last_interaction_time > 15000:  # 15 seconds
            if random.random() < 0.01:  # 1% chance per frame
                self.show_message("I miss you...")
                self.last_interaction_time = current_time
        
    def draw(self, surface):
        # Draw base (cloud-like shape)
        self.draw_cloud(surface, self.position, self.size)
        
        # Draw face based on state
        self.draw_face(surface)
        
        # Draw touch effect if active
        if self.touch_timer > 0:
            self.draw_touch_effect(surface)
            
        # Draw heart particles
        for particle in self.heart_particles:
            x, y, size, dx, dy = particle
            pygame.draw.circle(surface, (255, 150, 150), (int(x), int(y)), int(size))
            
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
            pygame.draw.arc(surface, (30, 30, 40), 
                           (x - self.size//3, y + self.size//4, self.size//1.5, self.size//3),
                           math.pi, 2*math.pi, 3)
            
        elif self.state == RobotState.SAD:
            # Sad eyes
            pygame.draw.circle(surface, (30, 30, 40), (x - eye_spacing, eye_y), eye_radius)
            pygame.draw.circle(surface, (30, 30, 40), (x + eye_spacing, eye_y), eye_radius)
            
            # Sad mouth
            pygame.draw.arc(surface, (30, 30, 40), 
                           (x - self.size//3, y + self.size//4, self.size//1.5, self.size//3),
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
        font = pygame.font.SysFont("Arial", 20)
        
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
        
        # Draw interaction level with a progress bar
        text = font.render(f"Connection: {self.interaction_level}%", True, (200, 200, 220))
        surface.blit(text, (20, 50))
        
        # Draw progress bar
        bar_width = 200
        bar_rect = pygame.Rect(20, 80, bar_width, 15)
        pygame.draw.rect(surface, (50, 50, 70), bar_rect, border_radius=7)
        fill_width = (bar_width * self.interaction_level) // 100
        fill_rect = pygame.Rect(20, 80, fill_width, 15)
        pygame.draw.rect(surface, (100, 180, 255), fill_rect, border_radius=7)
        
        # Draw streak
        if self.streak > 0:
            streak_text = f"Daily streak: {self.streak} days"
            text = font.render(streak_text, True, (255, 220, 100))
            surface.blit(text, (WIDTH - text.get_width() - 20, 20))
    
    def handle_click(self, pos):
        x, y = self.position
        distance = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
        
        if distance <= self.size:
            self.touch_timer = 30
            self.interaction_level = min(100, self.interaction_level + 2)
            self.last_interaction_time = pygame.time.get_ticks()
            
            # Create heart particles
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                self.heart_particles.append([x, y, random.uniform(3, 8), dx, dy])
            
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

# Create UI buttons
def create_buttons(robot):
    button_width = 150
    button_height = 50
    spacing = 20
    top_y = HEIGHT - button_height - 20
    
    buttons = [
        Button(20, top_y, button_width, button_height, "Happy", lambda: robot.change_mood(RobotState.HAPPY)),
        Button(20 + button_width + spacing, top_y, button_width, button_height, "Calm", lambda: robot.change_mood(RobotState.CALM)),
        Button(20 + 2*(button_width + spacing), top_y, button_width, button_height, "Neutral", lambda: robot.change_mood(RobotState.NEUTRAL)),
        Button(20 + 3*(button_width + spacing), top_y, button_width, button_height, "Message", lambda: robot.show_message())
    ]
    
    return buttons

# Create robot instance
robot = EmotionalRobot()
buttons = create_buttons(robot)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if not robot.handle_click(event.pos):
                    for button in buttons:
                        button.handle_event(event)
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
    
    # Update button hover states
    for button in buttons:
        button.check_hover(mouse_pos)
    
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
    
    # Draw UI buttons
    for button in buttons:
        button.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
