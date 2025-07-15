import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import re

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔸 At least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("🔸 Include uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔸 Include lowercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔸 Add digits (0-9)")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("🔸 Add special characters")

    if score <= 2:
        return "Weak", feedback
    elif score in [3, 4]:
        return "Moderate", feedback
    else:
        return "Strong", feedback

class PasswordCheckerApp(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=20, background_color="black"))

        self.label = toga.Label(
            "🔐 Enter your password:",
            style=Pack(font_size=16, margin_bottom=10, color="white")
        )

        self.input = toga.PasswordInput(style=Pack(margin=(5, 0, 10, 0)))

        self.button = toga.Button(
            "Check Strength",
            on_press=self.check_strength,
            style=Pack(
                background_color="red",
                color="white",
                padding=10,
                margin=(10, 0, 10, 0)
                # border_radius removed, not supported
            )
        )

        self.strength = toga.Label("", style=Pack(font_size=18, margin_top=10, color="white"))
        self.feedback = toga.Label("", style=Pack(font_size=14, margin_top=10, color="white"))

        main_box.add(self.label)
        main_box.add(self.input)
        main_box.add(self.button)
        main_box.add(self.strength)
        main_box.add(self.feedback)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def check_strength(self, widget):
        pwd = self.input.value
        result, tips = check_password_strength(pwd)

        color_map = {
            "Weak": "red",
            "Moderate": "orange",
            "Strong": "green"
        }

        self.strength.text = f"Password Strength: {result}"
        self.strength.style.color = color_map.get(result, "white")
        self.feedback.text = "\n".join(tips) if tips else "✅ Great password!"

def main():
    return PasswordCheckerApp("Password Strength Checker", "org.example.passwordchecker")

if __name__ == "__main__":
    main().main_loop()
