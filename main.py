from tkinter import Tk, Entry, Button, END
import subprocess
import pyttsx3
import speech_recognition as sr
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import plotille

voice_commands = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
    "divide": "/",
    "multiply": "*",
    "minus": "-",
    "plus": "+",
    "clear": "C",
    "equals": "=",
    "x": "x",
    "open parenthesis": "(",
    "close parenthesis": ")",
}

class Calculator:
    def __init__(self):
        # Initialize the GUI
        self.root = Tk()
        self.root.title("Voice Calculator")

        # Entry field for displaying the current input
        self.entry = Entry(self.root, width=16, borderwidth=5, font=("Arial", 20))
        self.entry.grid(row=0, column=0, columnspan=5)

        # Initialize classes for different functionalities
        self.input_handler = Input(self.entry)
        self.output_manager = Output(self.root, self.entry)

        # Create calculator buttons
        self.create_buttons()

    def create_buttons(self):
        button_labels = [
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "0",
            "/", "*", "-", "+", "C",
            "=", "x", "(", ")"
        ]

        row_val = 1
        col_val = 0

        for label in button_labels:
            if label == "=":
                button = Button(self.root, text=label, padx=20, pady=20, command=self.input_handler.calculate)
            elif label == "C":
                button = Button(self.root, text=label, padx=20, pady=20, command=self.input_handler.clear)
            elif label in ["x", "(", ")"]:
                button = Button(self.root, text=label, padx=20, pady=20, command=lambda l=label: self.input_handler.button_click(l))
            else:
                button = Button(self.root, text=label, padx=20, pady=20, command=lambda l=label: self.input_handler.button_click(l))

            button.grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # Create a voice recognition button
        voice_button = Button(self.root, text="Voice Recognition", padx=30, pady=20, command=self.input_handler.start_voice_recognition)
        voice_button.grid(row=row_val, column=col_val, columnspan=5, rowspan=2)

        # Create a "Delete" button
        delete_button = Button(self.root, text="Delete", padx=20, pady=20, command=self.input_handler.delete_last)
        delete_button.grid(row=row_val + 2, column=col_val, columnspan=5)

        # Create a "Plot Graph" button
        plot_graph_button = Button(self.root, text="Plot Graph", padx=20, pady=20, command=self.input_handler.plot_graph_from_entry)
        plot_graph_button.grid(row=row_val + 3, column=col_val, columnspan=5)

        # Create a "Plot Braille Graph" button
        plot_braille_graph_button = Button(self.root, text="Plot Braille Graph", padx=20, pady=20, command=self.input_handler.plot_braille_graph_from_entry)
        plot_braille_graph_button.grid(row=row_val + 4, column=col_val, columnspan=5)

    def run(self):
        # Main loop
        self.root.mainloop()

class Input:
    def __init__(self, entry):
        self.entry = entry
        self.recognizer = sr.Recognizer()
        self.graphing_calculator = Graph()
        self.tts_engine = pyttsx3.init()

    def button_click(self, value):
        if value.lower() == "c":
            self.clear()
        elif value.lower() == "=":
            self.calculate()
        else:
            current = self.entry.get()
            self.entry.delete(0, END)
            self.entry.insert(0, current + str(value))
            self.speak(str(value))

    def clear(self):
        self.entry.delete(0, END)
        self.speak("Cleared")

    def delete_last(self):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, current[:-1])
        self.speak("Deleted")

    def calculate(self):
        try:
            expression = self.entry.get()
            result = eval(expression)
            self.entry.delete(0, END)
            self.entry.insert(0, result)
            self.speak(f"The result is {result}")
        except Exception as e:
            self.entry.delete(0, END)
            self.entry.insert(0, "Error")
            self.speak("Error")

    def speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def voice_recognition(self):
        with sr.Microphone() as source:
            print("Listening for a voice command...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio).lower()
                if command in voice_commands:
                    self.button_click(voice_commands[command])
                else:
                    self.speak("Voice command not recognized")
            except sr.UnknownValueError:
                self.speak("Voice command not recognized")
            except sr.RequestError as e:
                self.speak(f"Could not request results: {e}")
            except Exception as e:
                self.speak(f"An error occurred: {e}")

    def start_voice_recognition(self):
        # Schedule the voice recognition method to run after 100 milliseconds
        self.entry.after(100, self.voice_recognition)

    def plot_graph(self, equation_str):
        try:
            self.graphing_calculator.plot_graph(equation_str)
            self.speak("Graph plotted")
        except Exception as e:
            self.entry.delete(0, END)
            self.entry.insert(0, f"Error: {e}")
            self.speak(f"Error: {e}")

    def plot_braille_graph(self, equation_str):
        try:
            self.graphing_calculator.plot_braille_graph(equation_str)
            self.speak("Braille Graph plotted")
        except Exception as e:
            self.entry.delete(0, END)
            self.entry.insert(0, f"Error: {e}")
            self.speak(f"Error: {e}")

    def plot_graph_from_entry(self):
        expression_str = self.entry.get()
        self.plot_graph(expression_str)

    def plot_braille_graph_from_entry(self):
        expression_str = self.entry.get()
        self.plot_braille_graph(expression_str)

class Output:
    def __init__(self, root, entry):
        self.root = root
        self.entry = entry

    # Add methods for managing output display here

class Graph:
    def __init__(self):
        pass

    def plot_graph(self, equation_str):
        x = np.linspace(-10, 10, 400)
        equation = sp.sympify(equation_str)
        y = sp.lambdify('x', equation, 'numpy')(x)
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Graph of {equation_str}')
        plt.grid(True)
        plt.show()

    def plot_braille_graph(self, equation_str):
        x = np.linspace(-10, 10, 400)
        equation = sp.sympify(equation_str)
        y = sp.lambdify('x', equation, 'numpy')(x)

        # Plotting using plotille (Braille graph)
        fig = plotille.Figure()
        fig.width = 80
        fig.height = 30
        fig.set_x_limits(min_=min(x), max_=max(x))
        fig.set_y_limits(min_=min(y), max_=max(y))
        fig.color_mode = 'byte'
        fig.plot(x, y, lc=25, label='Graph')
        print(fig.show(legend=True))

# Instantiate and run the calculator
calculator = Calculator()
calculator.run()
