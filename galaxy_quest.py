from __future__ import annotations

from array import array
import math
from pathlib import Path


try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None

try:
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate
except ImportError:  # pragma: no cover
    getSampleStyleSheet = None
    Paragraph = None
    SimpleDocTemplate = None


QUESTIONS = [
    ("Which planet is known as the Red Planet?", ["Moon", "Earth", "Mars", "Sun"], "mars", "c"),
    ("Which is the closest star to Earth?", ["Sirius", "Polaris", "The Sun", "Saturn"], "the sun", "c"),
    ("Which planet is the largest in our Solar System?", ["Neptune", "Uranus", "Jupiter", "Saturn"], "jupiter", "c"),
    ("Which is the closest star to Earth besides the Sun?", ["Sirius", "Polaris", "Jupiter", "Saturn"], "sirius", "a"),
    ("Which planet is closest to the Sun?", ["Venus", "Mercury", "Earth", "Mars"], "mercury", "b"),
    ("Which force keeps planets orbiting the Sun?", ["Wind", "Gravity", "Magnetism", "Electricity"], "gravity", "b"),
    ("Which planet is famous for the Great Red Spot?", ["Jupiter", "Saturn", "Neptune", "Uranus"], "jupiter", "a"),
    ("What do astronauts wear in space?", ["Raincoat", "Jacket", "Spacesuit", "Armor"], "spacesuit", "c"),
    ("Which galaxy contains our Solar System?", ["Andromeda", "Whirlpool", "Milky Way", "Sombrero"], "milky way", "c"),
    ("Which is the hottest planet in our Solar System?", ["Mercury", "Venus", "Mars", "Earth"], "venus", "b"),
    ("Which planet is known for its icy blue color?", ["Neptune", "Mars", "Mercury", "Venus"], "neptune", "a"),
    ("What is a shooting star actually called?", ["Meteor", "Planet", "Moon", "Comet"], "meteor", "a"),
    ("Which is the first planet from the Sun?", ["Earth", "Mercury", "Venus", "Mars"], "mercury", "b"),
    ("Which planet is called Earth's twin?", ["Venus", "Mars", "Jupiter", "Saturn"], "venus", "a"),
    ("Who was the first human to walk on the Moon?", ["Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Alan Shepard"], "neil armstrong", "b"),
    ("Which dwarf planet was once considered the ninth planet?", ["Ceres", "Pluto", "Eris", "Haumea"], "pluto", "b"),
    ("Which planet spins on its side?", ["Mars", "Uranus", "Jupiter", "Venus"], "uranus", "b"),
    ("What is the name of our Solar System's star?", ["Polaris", "Sirius", "The Sun", "Betelgeuse"], "the sun", "c"),
    ("Which planet has the strongest winds?", ["Saturn", "Neptune", "Mars", "Venus"], "neptune", "b"),
    ("Which planet has the most known moons?", ["Earth", "Saturn", "Mars", "Venus"], "saturn", "b"),
    ("Which object has a glowing tail when near the Sun?", ["Comet", "Asteroid", "Moon", "Meteorite"], "comet", "a"),
    ("Which telescope was launched in 2021?", ["Kepler", "Hubble", "James Webb Space Telescope", "Chandra"], "james webb space telescope", "c"),
    ("Which planet has the shortest year?", ["Mercury", "Earth", "Mars", "Venus"], "mercury", "a"),
    ("What was the first artificial satellite launched into space?", ["Apollo 11", "Voyager 1", "Sputnik 1", "Hubble"], "sputnik 1", "c"),
    ("Which planet is called the Blue Planet?", ["Mars", "Earth", "Neptune", "Uranus"], "earth", "b"),
    ("How many planets are in our Solar System?", ["7", "8", "9", "10"], "8", "b"),
    ("Which is the largest type of star among these choices?", ["Red Dwarf", "White Dwarf", "Red Supergiant", "Brown Dwarf"], "red supergiant", "c"),
    ("Which planet is famous for its icy blue color?", ["Mercury", "Uranus", "Venus", "Earth"], "uranus", "b"),
    ("What do we call a large group of stars held together by gravity?", ["Planet", "Galaxy", "Asteroid", "Moon"], "galaxy", "b"),
    ("Which object travels around a planet?", ["Star", "Satellite", "Galaxy", "Comet"], "satellite", "b"),
    ("What is the tallest volcano in the Solar System?", ["Mount Everest", "Olympus Mons", "Mauna Loa", "Mount Fuji"], "olympus mons", "b"),
    ("Which planet is the smallest?", ["Pluto", "Mercury", "Mars", "Venus"], "mercury", "b"),
    ("What is the most abundant element in the universe?", ["Iron", "Hydrogen", "Oxygen", "Rock"], "hydrogen", "b"),
    ("Which planet has no moons?", ["Earth", "Venus", "Jupiter", "Saturn"], "venus", "b"),
    ("What is a space rock that orbits the Sun called?", ["Asteroid", "Meteor", "Moon", "Star"], "asteroid", "a"),
    ("Which planet takes the longest to orbit the Sun?", ["Jupiter", "Neptune", "Saturn", "Uranus"], "neptune", "b"),
    ("What is the bright path of stars across the night sky called?", ["Orion", "Milky Way", "Andromeda", "Ring Galaxy"], "milky way", "b"),
    ("What protects Earth from harmful solar radiation?", ["Clouds", "Magnetic Field", "Mountains", "Oceans"], "magnetic field", "b"),
    ("Which planet has the fastest winds after Neptune?", ["Saturn", "Mercury", "Earth", "Venus"], "saturn", "a"),
    ("Which is the center of our Solar System?", ["Earth", "Jupiter", "The Sun", "Moon"], "the sun", "c"),
    ("What do astronauts experience because of very weak gravity?", ["Heavy Weight", "Weightlessness", "Super Speed", "Darkness"], "weightlessness", "b"),
    ("What planet is famous for its giant ring system?", ["Saturn", "Mars", "Earth", "Mercury"], "saturn", "a"),
    ("What is a scientist who studies space called?", ["Geologist", "Astronomer", "Biologist", "Chemist"], "astronomer", "b"),
    ("Which planet has a day longer than its year?", ["Venus", "Earth", "Mars", "Jupiter"], "venus", "a"),
    ("Which moon is the largest in the Solar System?", ["Titan", "Ganymede", "Europa", "Luna"], "ganymede", "b"),
    ("Who was the first woman in space?", ["Sally Ride", "Valentina Tereshkova", "Mae Jemison", "Christina Koch"], "valentina tereshkova", "b"),
    ("Which gas giant has the Great Red Spot?", ["Saturn", "Jupiter", "Uranus", "Neptune"], "jupiter", "b"),
    ("What is a collection of billions of galaxies called?", ["Solar System", "Constellation", "Universe", "Orbit"], "universe", "c"),
    ("Which planet has the highest mountain in the Solar System?", ["Earth", "Mars", "Venus", "Mercury"], "mars", "b"),
    ("Which planet is farthest from the Sun?", ["Saturn", "Uranus", "Neptune", "Jupiter"], "neptune", "c"),
]


def get_rank(score: int) -> str:
    percentage = score / len(QUESTIONS)
    if percentage >= 0.9:
        return "Space Master"
    if percentage >= 0.7:
        return "Space Explorer"
    if percentage >= 0.5:
        return "Cadet"
    return "Rookie"


def normalize_answer(value: str) -> str:
    """Make answer matching case-insensitive and ignore extra spaces."""
    return " ".join(value.strip().casefold().split())


SAMPLE_RATE = 44_100
ANSWER_SOUNDS: dict[str, object] = {}
sound_ready = False
LAST_RESULTS: dict[str, object] | None = None


def make_game_sound(notes):
    """Create a short, original game-style jingle for pygame to play."""
    samples = array("h")
    for frequency, duration in notes:
        total_samples = int(SAMPLE_RATE * duration)
        for index in range(total_samples):
            progress = index / total_samples
            envelope = min(1, progress * 25, (1 - progress) * 18)
            wave = math.sin(2 * math.pi * frequency * index / SAMPLE_RATE)
            harmonic = 0.25 * math.sin(4 * math.pi * frequency * index / SAMPLE_RATE)
            value = int((wave + harmonic) * envelope * 7_000)
            samples.extend((value, value))
    return pygame.mixer.Sound(buffer=samples.tobytes())


def prepare_answer_sounds() -> bool:
    """Set up pygame once and keep the sounds ready for the whole quiz."""
    global sound_ready
    if sound_ready or pygame is None:
        return sound_ready

    try:
        pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
        pygame.mixer.init()
        ANSWER_SOUNDS["correct"] = make_game_sound([(659, 0.08), (784, 0.08), (1047, 0.20)])
        ANSWER_SOUNDS["incorrect"] = make_game_sound([(392, 0.14), (330, 0.20)])
        sound_ready = True
    except Exception:
        sound_ready = False
    return sound_ready


def play_answer_sound(is_correct: bool) -> None:
    if not prepare_answer_sounds():
        return
    key = "correct" if is_correct else "incorrect"
    snd = ANSWER_SOUNDS.get(key)
    if snd is not None:
        snd.play()


def play_title_music() -> None:
    """Play a short title jingle."""
    if prepare_answer_sounds():
        melody = make_game_sound([(523, 0.12), (659, 0.12), (784, 0.18), (1047, 0.25)])
        melody.play()


def play_game_over_music() -> None:
    """Play a game over tune."""
    if prepare_answer_sounds():
        melody = make_game_sound([(392, 0.20), (349, 0.20), (294, 0.25), (262, 0.35)])
        melody.play()


def play_victory_music() -> None:
    """Play a victory tune."""
    if prepare_answer_sounds():
        melody = make_game_sound([(523, 0.10), (659, 0.10), (784, 0.10), (1047, 0.35)])
        melody.play()


def save_results(name: str, score: int, hearts: int, streak: int, correct: int, incorrect: int) -> None:
    global LAST_RESULTS

    LAST_RESULTS = {
        "name": name,
        "score": score,
        "hearts": hearts,
        "streak": streak,
        "correct": correct,
        "incorrect": incorrect,
        "rank": get_rank(score),
    }

    if SimpleDocTemplate is None:
        print("PDF results were skipped because reportlab is not installed.")
        return

    filename = Path("Galaxy Quest Quiz Results.pdf")
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(str(filename))

    results = [
        Paragraph("Galaxy Quest Results", styles["Heading1"]),
        Paragraph(f"Player: {name}", styles["BodyText"]),
        Paragraph(f"Score: {score}/{len(QUESTIONS)}", styles["BodyText"]),
        Paragraph(f"Rank: {get_rank(score)}", styles["BodyText"]),
        Paragraph(f"Correct: {correct}", styles["BodyText"]),
        Paragraph(f"Incorrect: {incorrect}", styles["BodyText"]),
        Paragraph(f"Hearts Remaining: {hearts}", styles["BodyText"]),
        Paragraph(f"Best Streak: {streak}", styles["BodyText"]),
    ]

    document.build(results)
    print(f"\nResults saved to {filename}")


def show_how_to_play() -> None:
    print("\n========== HOW TO PLAY ==========")
    print("• Answer with A, B, C or D.")
    print("• You may also type the full answer.")
    print("• You start with 5 hearts.")
    print("• Every wrong answer loses one heart.")
    print("• Reach 0 hearts and the game ends.")
    input("\nPress Enter to return...")


def show_credits():
    print("\n" + "=" * 60)
    print("                 🌌 GALAXY QUEST 🌌")
    print("          Ultimate Space Quiz Game")
    print("                  Version 2.0")
    print("=" * 60)

    print("\n🎮 GAME INFORMATION")
    print("Game Name        : Galaxy Quest")
    print("Genre            : Educational Space Quiz")
    print("Purpose          : Learning and Quiz Preparation")
    print("Programming Lang.: Python")
    print("Version          : 2.0")

    print("\n📚 ABOUT THE PROGRAM")
    print("Galaxy Quest is an educational quiz application")
    print("designed to help students improve their")
    print("knowledge of astronomy and space science.")
    print()
    print("It can be used for:")
    print("• Learning new space facts")
    print("• School revision")
    print("• Test and quiz preparation")
    print("• Classroom practice")
    print("• General knowledge improvement")

    print("\n👨‍💻 DEVELOPMENT")
    print("Game Creator     : Hamza")
    print("Lead Programmer  : Hamza")
    print("Game Designer    : Hamza")
    print("Question Writer  : Hamza")
    print("Game Tester      : Hamza")

    print("\n🛠 TECHNOLOGIES USED")
    print("• Python")
    print("• Pygame")
    print("• ReportLab")

    print("\n🎵 AUDIO")
    print("Original game sounds generated using Python.")
    print("No copyrighted music is included.")

    print("\n⭐ FEATURES")
    print("• 50 Space Questions")
    print("• Multiple Choice Quiz")
    print("• Hearts System")
    print("• Score System")
    print("• Streak Counter")
    print("• Player Ranking")
    print("• PDF Result Generator")
    print("• Sound Effects")
    print("• Main Menu")

    print("\n🙏 SPECIAL THANKS")
    print("• Allah (SWT)")
    print("• My Parents")
    print("• My Teachers")
    print("• Everyone who plays Galaxy Quest")

    print("\n© 2026 Hamza")
    print("Galaxy Quest is an educational application")
    print("created for learning and test preparation.")

    print("\n🚀 Thank you for playing Galaxy Quest!")
    print("Keep learning, keep exploring the universe!")

    print("=" * 60)

    input("\nPress Enter to return to the Main Menu...")


def show_previous_results() -> None:
    print("\n========== PREVIOUS RESULTS ==========")

    if LAST_RESULTS is None:
        print("No results available yet.")
    else:
        print(f"Player: {LAST_RESULTS['name']}")
        print(f"Score: {LAST_RESULTS['score']}/{len(QUESTIONS)}")
        print(f"Rank: {LAST_RESULTS['rank']}")
        print(f"Correct: {LAST_RESULTS['correct']}")
        print(f"Incorrect: {LAST_RESULTS['incorrect']}")

    input("\nPress Enter to return...")


def title_screen() -> None:
    print("=" * 45)
    print("          🌌 GALAXY QUEST 🌌")
    print("        Ultimate Space Quiz")
    print("=" * 45)


def main_menu() -> None:
    while True:
        title_screen()
        # Ensure title music plays (if audio is available)
        play_title_music()

        print("\nMain Menu")
        print("1. ▶ Start Game")
        print("2. 📖 How To Play")
        print("3. 👨‍🚀 Credits")
        print("4. ❌ Exit")
        print("5. 📄 Previous Results")

        choice = input("\nChoose (1-5): ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            show_how_to_play()
        elif choice == "3":
            show_credits()
        elif choice == "4":
            print("\nThanks for playing Galaxy Quest!")
            break
        elif choice == "5":
            show_previous_results()
        else:
            print("\nInvalid choice!")

        input("\nPress Enter to continue...")


def play_game() -> None:
    name = input("Write your name: ").strip() or "Player"
    hearts = 5
    score = 0
    streak = 0
    correct = 0
    incorrect = 0

    print(f"Hello, {name}! Answer with A, B, C, D, or the full answer.")

    for number, (question, options, answer, letter) in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}/{len(QUESTIONS)}: {question}")
        for option_letter, option in zip("abcd", options):
            print(f"{option_letter.upper()}: {option}")

        user_answer = normalize_answer(input("Answer: "))
        is_correct = user_answer == normalize_answer(answer) or user_answer == normalize_answer(letter)

        if is_correct:
            print("Correct!")
            play_answer_sound(is_correct=True)
            score += 1
            correct += 1
            streak += 1
        else:
            print(f"Incorrect. The correct answer is {answer.title()}.")
            play_answer_sound(is_correct=False)
            hearts -= 1
            incorrect += 1
            streak = 0

            if hearts <= 0:
                hearts = 0
                print("\n💀 GAME OVER 💀")
                play_game_over_music()
                break

    rank = get_rank(score)
    print(f"\n{rank}")
    if hearts > 0:
        print(f"{name}, you finished the quiz!")
        play_victory_music()
    else:
        print(f"Good try, {name}. You ran out of hearts.")

    save_results(name, score, hearts, streak, correct, incorrect)

def main():
    main_menu()

if __name__ == "__main__":
    main()
