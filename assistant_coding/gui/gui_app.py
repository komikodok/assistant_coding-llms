import tkinter as tk
from assistant_coding.gui import ChatbotFrame
from assistant_coding.gui import TerminalFrame


class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with ...")

        # Frame utama
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Inisialisasi Terminal dan Chatbot App
        self.chatbot_frame = ChatbotFrame(self.main_frame)
        self.terminal_frame = TerminalFrame(self.main_frame, self.chatbot_frame)

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenmmwidth()
    screen_height = root.winfo_screenmmheight()

    root.geometry(f"400x400+{screen_width//2}+{screen_height//2}")
    app = InterfaceApp(root)
    root.mainloop()