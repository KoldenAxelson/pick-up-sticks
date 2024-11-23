# Pick-up Sticks PyGame

A simple grid-based collection game built with PyGame, demonstrating core game development concepts like collision detection, smooth movement, and state management.

## 🎮 Features

- Grid-based movement system with smooth transitions
- Player-centered camera that follows movement
- Collision detection with obstacles
- Running mechanics (hold shift)
- Score tracking system
- Randomly generated obstacles
- Bounded play area

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- PyGame

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/pick-up-sticks.git
cd pick-up-sticks
```

2. Create a virtual environment
```bash
python3 -m venv venv
```

3. Activate the virtual environment
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies
```bash
pip install pygame
```

5. Run the game
```bash
python main.py
```

## 🕹️ Controls

- **W**: Move up
- **A**: Move left
- **S**: Move down
- **D**: Move right
- **SPACE**: Interact with sticks
- **LEFT SHIFT**: Run
- **ESC**: Quit game

## 🎯 Game Objectives

- Move around the grid to collect sticks
- Navigate around rocks and obstacles
- Cannot move through obstacles or off the map
- Must be adjacent to sticks to collect them

## 💡 Learning Concepts

This project demonstrates several key PyGame concepts:

- Sprite movement and control
- Grid-based collision detection
- Camera systems
- Game state management
- Event handling
- Frame rate independent movement
- Random object generation

## 🛠️ Technical Implementation

Key technical features include:
- Frame-rate independent movement using delta time
- Grid-based collision system
- Smooth transition between grid positions
- State-based player coloring
- Camera offset calculations
- Bounded map generation

## 🤝 Contributing

Feel free to fork this project and submit pull requests. You can also open issues for bugs or feature suggestions.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PyGame documentation and community
- Grid-based game design patterns
- Python virtual environment best practices