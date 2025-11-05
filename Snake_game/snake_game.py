import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_ITEM_SIZE = 20
MIN_SPEED = 50

BACKGROUND_COLOR = "#000"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
MEGA_FOOD_COLOR = "#FFD700"
OBSTACLE_COLOR = "#808080"

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}

DIFFICULTY_SETTINGS = {
    "Easy": {"speed": 200, "step": 10},
    "Medium": {"speed": 150, "step": 15},
    "Hard": {"speed": 100, "step": 20}
}

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        self.canvas = tk.Canvas(master, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        control_frame = tk.Frame(master)
        control_frame.pack()

        tk.Label(control_frame, text="Difficulty:").pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="Medium")
        self.difficulty_menu = tk.OptionMenu(control_frame, self.difficulty_var, *DIFFICULTY_SETTINGS.keys())
        self.difficulty_menu.pack(side=tk.LEFT)

        tk.Label(control_frame, text=" Map:").pack(side=tk.LEFT)
        self.map_var = tk.StringVar(value="No Obstacles")
        self.map_menu = tk.OptionMenu(control_frame, self.map_var, "No Obstacles", "With Obstacles")
        self.map_menu.pack(side=tk.LEFT)

        self.restart_button = tk.Button(control_frame, text="Start / Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT)

        self.label = tk.Label(master, text="", font=("Arial", 14))
        self.label.pack()

        self.high_score_label = tk.Label(master, text="High Score: 0", font=("Arial", 12))
        self.high_score_label.pack()

        self.master.bind("<KeyPress>", self.change_direction)

        self.high_score = 0
        self.running = False

    def restart_game(self):
        self.canvas.delete("all")
        self.running = True
        self.score = 0
        self.food_eaten = 0
        self.mega_food = None
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)]

        difficulty = self.difficulty_var.get()
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Medium"])
        self.speed = settings["speed"]
        self.speed_step = settings["step"]

        self.generate_map()
        self.spawn_food()
        self.update_labels()
        self.move_snake()

    def update_labels(self):
        self.label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    # 1️⃣ Generate obstacles if selected
    def generate_map(self):
        self.obstacles = []
        map_type = self.map_var.get()
        if map_type == "With Obstacles":
            for i in range(100, 500, 100):
                self.obstacles.append((i, 200))
            for j in range(120, 300, 40):
                self.obstacles.append((300, j))
        self.draw_obstacles()

    def draw_obstacles(self):
        self.canvas.delete("obstacle")
        for x, y in self.obstacles:
            self.canvas.create_rectangle(
                x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE,
                fill=OBSTACLE_COLOR, tags="obstacle"
            )

    # 2️⃣ Snake movement and collisions
    def move_snake(self):
        if not self.running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = DIRECTIONS[self.direction]
        new_head = (head_x + dx * SNAKE_ITEM_SIZE, head_y + dy * SNAKE_ITEM_SIZE)

        if self.check_collision(new_head):
            self.game_over()
            return

        self.snake = [new_head] + self.snake

        # 3️⃣ Handle food and mega food
        if new_head == self.food:
            self.score += 1
            self.food_eaten += 1
            self.canvas.delete("food")
            if self.food_eaten % 4 == 0:
                self.spawn_mega_food()
            else:
                self.spawn_food()
            self.increase_speed()
        elif self.mega_food and new_head == self.mega_food:
            self.score += 3
            self.mega_food = None
            self.canvas.delete("mega_food")
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw_snake()
        self.update_labels()
        self.master.after(self.speed, self.move_snake)

    # 4️⃣ Draw snake on canvas
    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE,
                fill=SNAKE_COLOR, tags="snake"
            )

    # 5️⃣ Random food spawns avoiding obstacles
    def spawn_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            y = random.randint(0, (GAME_HEIGHT - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                self.food = (x, y)
                break
        self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + SNAKE_ITEM_SIZE, self.food[1] + SNAKE_ITEM_SIZE,
            fill=FOOD_COLOR, tags="food"
        )

    def spawn_mega_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            y = random.randint(0, (GAME_HEIGHT - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                self.mega_food = (x, y)
                break
        self.canvas.create_oval(
            self.mega_food[0], self.mega_food[1],
            self.mega_food[0] + SNAKE_ITEM_SIZE, self.mega_food[1] + SNAKE_ITEM_SIZE,
            fill=MEGA_FOOD_COLOR, tags="mega_food"
        )

    def check_collision(self, head):
        x, y = head
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        if head in self.snake:
            return True
        if head in self.obstacles:
            return True
        return False

    def increase_speed(self):
        if self.score % 5 == 0 and self.speed > MIN_SPEED:
            self.speed -= self.speed_step
            if self.speed < MIN_SPEED:
                self.speed = MIN_SPEED

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 2,
            text="Game Over!", fill="white", font=("Arial", 24)
        )
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_labels()

    def change_direction(self, event):
        key = event.keysym
        if key not in DIRECTIONS:
            return
        dx, dy = DIRECTIONS[key]
        cur_dx, cur_dy = DIRECTIONS[self.direction]
        if dx == -cur_dx and dy == -cur_dy:
            return
        self.next_direction = key

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
