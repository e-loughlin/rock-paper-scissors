import math
import os
import random

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)


def distance(unit1, unit2):
    """Calculate the Euclidean distance between two units."""
    return math.hypot(unit1.x - unit2.x, unit1.y - unit2.y)


# Load your images (ensure these are in the correct folder)
ROCK_IMAGE = pygame.image.load(os.path.join("images", "rock.png"))
PAPER_IMAGE = pygame.image.load(os.path.join("images", "paper.png"))
SCISSORS_IMAGE = pygame.image.load(os.path.join("images", "scissors.png"))

# Scaling the images (optional, depending on the image size)
ROCK_IMAGE = pygame.transform.scale(ROCK_IMAGE, (40, 40))
PAPER_IMAGE = pygame.transform.scale(PAPER_IMAGE, (40, 40))
SCISSORS_IMAGE = pygame.transform.scale(SCISSORS_IMAGE, (40, 40))


class Unit:
    def __init__(self, unit_type, x, y):
        self.unit_type = unit_type
        self.x = x
        self.y = y
        self.speed = 2
        self.size = 40

        # Load the corresponding image for the unit type
        if self.unit_type == "rock":
            self.image = ROCK_IMAGE
        elif self.unit_type == "paper":
            self.image = PAPER_IMAGE
        elif self.unit_type == "scissors":
            self.image = SCISSORS_IMAGE

    def move(self, env):
        # Same move logic as before (chase and evade)
        target = None
        avoid = None
        if self.unit_type == "rock":
            target = self.find_closest(env, "scissors")  # Rock chases scissors
            avoid = self.find_closest(env, "paper")  # Rock evades paper
        elif self.unit_type == "paper":
            target = self.find_closest(env, "rock")  # Paper chases rock
            avoid = self.find_closest(env, "scissors")  # Paper evades scissors
        elif self.unit_type == "scissors":
            target = self.find_closest(env, "paper")  # Scissors chases paper
            avoid = self.find_closest(env, "rock")  # Scissors evades rock

        # Move towards the target
        if target:
            self.move_towards(target)

        # Move away from the unit to avoid
        if avoid:
            self.move_away_from(avoid)

    def draw(self, screen):
        """Draw the unit's image on the screen."""
        screen.blit(self.image, (self.x, self.y))

    def find_closest(self, env, unit_type):
        """Find the closest unit of a certain type."""
        closest_unit = None
        min_dist = float("inf")
        for unit in env.units:
            if unit.unit_type == unit_type:
                dist = distance(self, unit)
                if dist < min_dist:
                    min_dist = dist
                    closest_unit = unit
        return closest_unit

    def move_towards(self, target):
        """Move towards the target, ensuring not to go out of bounds considering the unit size."""
        # Move in the x-direction
        if target.x > self.x:
            new_x = self.x + self.speed
            if new_x + self.size < SCREEN_WIDTH:  # Check right boundary
                self.x = new_x
        elif target.x < self.x:
            new_x = self.x - self.speed
            if new_x > 0:  # Check left boundary
                self.x = new_x

        # Move in the y-direction
        if target.y > self.y:
            new_y = self.y + self.speed
            if new_y + self.size < SCREEN_HEIGHT:  # Check bottom boundary
                self.y = new_y
        elif target.y < self.y:
            new_y = self.y - self.speed
            if new_y > 0:  # Check top boundary
                self.y = new_y

    def move_away_from(self, target):
        """Move away from the target, ensuring not to go out of bounds considering the unit size."""
        # Move in the x-direction
        if target.x > self.x:
            new_x = self.x - self.speed
            if new_x > 0:  # Check left boundary
                self.x = new_x
        elif target.x < self.x:
            new_x = self.x + self.speed
            if new_x + self.size < SCREEN_WIDTH:  # Check right boundary
                self.x = new_x

        # Move in the y-direction
        if target.y > self.y:
            new_y = self.y - self.speed
            if new_y > 0:  # Check top boundary
                self.y = new_y
        elif target.y < self.y:
            new_y = self.y + self.speed
            if new_y + self.size < SCREEN_HEIGHT:  # Check bottom boundary
                self.y = new_y

    def interact(self, other_unit):
        """Interact with another unit, following game rules."""
        if self.unit_type == "rock" and other_unit.unit_type == "scissors":
            other_unit.unit_type = "rock"
            other_unit.image = ROCK_IMAGE
        elif self.unit_type == "scissors" and other_unit.unit_type == "paper":
            other_unit.unit_type = "scissors"
            other_unit.image = SCISSORS_IMAGE
        elif self.unit_type == "paper" and other_unit.unit_type == "rock":
            other_unit.unit_type = "paper"
            other_unit.image = PAPER_IMAGE

    def check_collision(self, other_unit):
        """Check if two units are 'touching' based on distance."""
        return distance(self, other_unit) < self.size


class Environment:
    def __init__(self):
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)

    def update(self):
        # Move and check interactions for all units
        for unit in self.units:
            unit.move(self)  # Pass the environment to the move method
            for other_unit in self.units:
                if unit != other_unit and unit.check_collision(other_unit):
                    unit.interact(other_unit)

    def draw(self, screen):
        for unit in self.units:
            unit.draw(screen)


# Initialize the game environment
env = Environment()

# Add some initial units (rock, paper, scissors)
for _ in range(10):
    env.add_unit(
        Unit("rock", random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    )
    env.add_unit(
        Unit("paper", random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    )
    env.add_unit(
        Unit(
            "scissors",
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
        )
    )

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors Simulation")

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events (e.g., quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update environment (move units, check interactions)
    env.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the environment and units
    env.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game when the loop ends
pygame.quit()
