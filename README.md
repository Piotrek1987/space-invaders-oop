# 🛸 Space Invaders – OOP Edition

A modern, object-oriented Python take on the classic **Space Invaders** game, created as part of the "100 Days of Code" challenge.

---

## 🎮 Features

- ✅ Smooth player movement and bullet mechanics  
- 👾 Diverse enemy types:
  - Zigzag, Dive, Teleport, Tank, Fast, Rare, and Boss Aliens
- 🌊 Wave-based enemy spawning system
- 💥 Challenging difficulty that scales over time
- 🧠 Strategic resource management (ammo, lives)
- 🔮 Power-ups system with effects like:
  - 🛡️ 2 extra lives / with max lives extra ammo
  - 💊 Health restore / with max lives explode all enemies
  - ❄️ Explode all enemies
  - 💥 Clone Ship — spawn two extra ships for 20 seconds!
- 🎨 Modular assets loading
- 🧱 Object-Oriented Programming design (great for learning or extending)

---

## 🚀 Controls

| Action        | Key            |
|---------------|----------------|
| Move Left     | ⬅️ / A          |
| Move Right    | ➡️ / D          |
| Shoot Bullet  | Spacebar       |
| Quit Game     | ESC            |

---

## 🧱 Code Structure

```
├── main.py               # Game entry point
├── game.py               # Main game loop and core logic
├── player.py             # Player class, movement, shooting, clones
├── enemy.py              # All enemy types and behaviors
├── bullet.py             # Bullet class
├── powerup.py            # Power-up types and effects
├── assets.py             # Loads images and assets
├── settings.py           # Global constants like screen size and lives
├── img/                  # Image assets (player, aliens, power-ups)
├── README.md             # Project documentation
└── requirements.txt      # Python package dependencies
```

---

## 🖼️ Assets

All visual assets are stored in the `img/` directory and loaded via `assets.py`. Power-up icons are mapped like this:

```python
powerup_images = {
    "health": pygame.image.load("img/medical-kit.png").convert_alpha(),
    "ammo": pygame.image.load("img/bullet.png").convert_alpha(),
    "shield": pygame.image.load("img/shield.png").convert_alpha(),
    "slow": pygame.image.load("img/frozen.png").convert_alpha(),
    "clone": pygame.image.load("img/ship-clone.png").convert_alpha()
}
```

To replace or add new graphics, just swap the image files and update the mapping.

---

## 📦 Installation

1. **Make sure you have Python 3.8+ installed.**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the game:**

```bash
python main.py
```

---

## 📄 requirements.txt

```txt
pygame==2.5.2
```

---

## 🧬 Clone Ship Power-Up

This power-up creates two clones of the player's ship:

- 🛩️ One clone appears to the left, another to the right.
- 🧠 They follow the player's horizontal movement.
- 🔫 Each fires bullets at the same time, tripling firepower.
- ⚠️ Only the main ship can take damage.
- ⏱️ Clones disappear after 10 seconds.

---

## 💡 Ideas for Future Expansion

- 🌐 Online high score leaderboard
- 🎮 Gamepad/controller support
- 💾 Save/load game states
- 🛠️ Level editor
- 🔁 Endless mode
- 🎆 Explosions, sounds, and music

---

## 👤 Author

**Peter** – developed as part of the [100 Days of Code Challenge – Day 95+]

---

## 📜 License

Licensed under the MIT License.  
Free to use, modify, and distribute.

---

💻 Made with Python and Pygame — have fun defending the galaxy!
