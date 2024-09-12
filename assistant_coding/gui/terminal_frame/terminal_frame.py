import tkinter as tk
from tkinter import Scrollbar
import subprocess
import os

from threading import Thread
from langchain_core.messages import HumanMessage, AIMessage
from assistant_coding.llms.llm_app import LLMApp


class TerminalFrame:
    def __init__(self, root, chatbot_frame):
        self.chatbot_frame = chatbot_frame
        self.llm_app = LLMApp()

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Scrollbar vertikal untuk terminal
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Widget Text untuk terminal output dan input
        self.text = tk.Text(self.frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, bg="black", fg="white")
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.bind('<Return>', self.execute_command)

        # Menghubungkan scrollbar dengan Text widget
        self.scrollbar.config(command=self.text.yview)

        # Inisialisasi dengan working directory di terminal
        self.insert_prompt()

    def insert_prompt(self):
        # Menampilkan awalan dengan current working directory di terminal
        cwd = os.getcwd()
        self.text.insert(tk.END, f"{cwd}$ ")
        self.text.mark_set("insert", "end-1c")
        self.text.see(tk.END)

    def execute_command(self, event=None):
        def threading_llm(user_input):
            # Freeze tombol dan entry ketika proses threading llm_invoke
            self.chatbot_frame.freeze_button_entry_while_threading() # Method dari class ChatbotFrame
            self.text.bind('<Return>', self.chatbot_frame.pass_process())

            llm_response = self.llm_app.invoke(
                question=user_input, 
                chat_history=self.chatbot_frame.chat_history, # Atribute dari class ChatbotFrame
                from_terminal=True
            )
            response_items = llm_response.get_response_items()
            # Menampilkan response bot ke dalam chatbot
            self.chatbot_frame.add_message(f"Bot: {response_items['generation']}") # Method dari class ChatbotFrame
            # Tambahkan ke chat history
            self.chatbot_frame.chat_history.append(HumanMessage(content=response_items['question'])) # Atribute dari class ChatbotFrame
            self.chatbot_frame.chat_history.append(AIMessage(content=response_items['generation'])) # Atribute dari class ChatbotFrame

            self.chatbot_frame.loading_frame.grid_forget() # Method dari class ChatbotFrame

            # Mengembalikan tombol dan entry ke dalam keadaan semula setelah proses threading_llm
            self.chatbot_frame.return_button_entry_after_threading() # Method dari class ChatbotFrame
            self.text.bind('<Return>', self.execute_command)

        # Mendapatkan perintah yang dimasukkan oleh pengguna di terminal
        command = self.get_input_command()
        if command.strip():
            # Pindah ke baris baru sebelum menampilkan output
            self.text.insert(tk.END, "\n")
            self.text.see(tk.END)

            # Menjalankan perintah
            terminal_run = subprocess.run(command, shell=True, text=True, capture_output=True)

            output = terminal_run.stdout if terminal_run.stdout else terminal_run.stderr

            if output == terminal_run.stdout:
                # Menampilkan output di terminal
                self.text.insert(tk.END, output)
            else:                   
                # Menampilkan output error di terminal
                self.text.insert(tk.END, output)

                user_input = f"cara mengatasi {output}"
                # Menampilkan error dari terminal ke dalam chatbot
                self.chatbot_frame.add_message(f"You: {user_input}") # Method dari class ChatbotFrame

                self.chatbot_frame.loading_frame.grid(column=0, row=0) # Atribute dari class ChatbotFrame
                self.chatbot_frame.loading_screen() # Method dari class ChatbotFrame
                Thread(target=threading_llm, args=(user_input, )).start()


        # Pindah ke baris baru dan menampilkan prompt kembali
        self.text.insert(tk.END, "\n")
        self.insert_prompt()
        return "break"

    def get_input_command(self):
        # Mendapatkan teks yang diinput dari prompt terakhir hingga akhir teks
        command = self.text.get("end-1c linestart", "end-1c")
        return command.split("$ ", 1)[-1].strip()