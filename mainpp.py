import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import google.generativeai as genai
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
from threading import Thread
import queue
import time
from PIL import Image, ImageTk

class GeminiChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Chatbot Professional")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")
        
        # Setup Gemini API
        self.setup_gemini()
        
        # Variables for audio recording
        self.is_recording = False
        self.audio_data = []
        self.fs = 44100  # Sample rate
        self.recording_thread = None
        
        # Create GUI
        self.create_gui()
        
        # Initialize chat history
        self.chat_history = []
        
    def setup_gemini(self):
        try:
            # Use the provided API key
            api_key = "AIzaSyCC9DImXNPKNo6_b3zGHhjjX_8JTUsjT4U"
            
            if not api_key:
                raise ValueError("API key is required")
            
            genai.configure(api_key=api_key)
            
            # Setup model configuration
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
            
            # Initialize the correct model names
            self.text_model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",  # Updated model name
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            self.vision_model = genai.GenerativeModel(
                model_name="gemini-1.0-pro-vision",  # Updated model name
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Test the connection
            genai.list_models()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize Gemini API: {str(e)}")
            self.root.destroy()
    
    def create_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#4285f4")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.header_label = tk.Label(
            header_frame, 
            text="Gemini Chatbot", 
            font=("Helvetica", 16, "bold"), 
            fg="white", 
            bg="#4285f4"
        )
        self.header_label.pack(pady=10)
        
        # Chat display area
        self.chat_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.GROOVE)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_text = tk.Text(
            self.chat_frame, 
            wrap=tk.WORD, 
            font=("Helvetica", 12), 
            bg="white", 
            fg="black", 
            padx=10, 
            pady=10,
            state=tk.DISABLED
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.chat_text.config(yscrollcommand=scrollbar.set)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg="#f0f2f5")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg="#f0f2f5")
        button_frame.pack(side=tk.LEFT, padx=(0, 5))
        
        # Microphone button
        self.mic_button = tk.Button(
            button_frame,
            text="🎤",
            font=("Helvetica", 14),
            bg="#e0e0e0",
            fg="red",
            relief=tk.FLAT,
            command=self.toggle_recording
        )
        self.mic_button.pack(side=tk.TOP, pady=(0, 5))
        
        # File upload button
        self.upload_button = tk.Button(
            button_frame,
            text="📁",
            font=("Helvetica", 14),
            bg="#e0e0e0",
            relief=tk.FLAT,
            command=self.upload_file
        )
        self.upload_button.pack(side=tk.TOP)
        
        # Input text
        self.input_entry = tk.Text(
            input_frame,
            height=4,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg="white",
            fg="black"
        )
        self.input_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Helvetica", 12, "bold"),
            bg="#4285f4",
            fg="white",
            relief=tk.FLAT,
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(5, 0), fill=tk.Y)
        
        # Bind Enter key to send message
        self.input_entry.bind("<Return>", lambda event: self.send_message())
        
        # Status bar
        self.status_bar = tk.Label(
            main_frame,
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Helvetica", 10),
            bg="#e0e0e0"
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
            self.mic_button.config(fg="red", text="⏹️")
        else:
            self.stop_recording()
            self.mic_button.config(fg="black", text="🎤")
    
    def start_recording(self):
        self.is_recording = True
        self.audio_data = []
        self.recording_thread = Thread(target=self.record_audio)
        self.recording_thread.start()
        self.update_status("Recording... click button again to stop")
    
    def stop_recording(self):
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        
        # Save recording to temporary file
        audio_file = "temp_recording.wav"
        sf.write(audio_file, np.concatenate(self.audio_data), self.fs)
        
        # For demo, just add a note that audio was recorded
        self.input_entry.insert(tk.END, "\n[Audio recorded - would be transcribed here]")
        self.update_status("Recording complete")
    
    def record_audio(self):
        with sd.InputStream(samplerate=self.fs, channels=1, dtype='float32', 
                          callback=self.audio_callback):
            while self.is_recording:
                time.sleep(0.1)
    
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.audio_data.append(indata.copy())
    
    def upload_file(self):
        filetypes = [
            ("All supported files", "*.jpg *.jpeg *.png *.pdf *.txt *.docx"),
            ("Image files", "*.jpg *.jpeg *.png"),
            ("Document files", "*.pdf *.txt *.docx"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if file_path:
            try:
                # For images, show preview
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.show_image_preview(file_path)
                else:
                    # For documents, just show the filename
                    self.input_entry.insert(tk.END, f"\n[File attached: {os.path.basename(file_path)}]")
                
                self.uploaded_file = file_path
                self.update_status(f"File selected: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def show_image_preview(self, image_path):
        try:
            # Open image and resize for preview
            image = Image.open(image_path)
            image.thumbnail((200, 200))
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Image Preview")
            
            # Convert to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            
            # Display image
            label = tk.Label(preview_window, image=photo)
            label.image = photo  # Keep reference
            label.pack(padx=10, pady=10)
            
            # Add confirmation button
            confirm_button = tk.Button(
                preview_window,
                text="Use This Image",
                command=lambda: self.confirm_image(image_path, preview_window)
            )
            confirm_button.pack(pady=(0, 10))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def confirm_image(self, image_path, window):
        self.input_entry.insert(tk.END, f"\n[Image attached: {os.path.basename(image_path)}]")
        window.destroy()
    
    def send_message(self):
        user_input = self.input_entry.get("1.0", tk.END).strip()
        if not user_input and not hasattr(self, 'uploaded_file'):
            return
            
        # Display user message in chat
        self.display_message("You", user_input)
        
        # Clear input
        self.input_entry.delete("1.0", tk.END)
        
        # Send to Gemini API in a separate thread
        Thread(target=self.process_with_gemini, args=(user_input,)).start()
    
    def process_with_gemini(self, user_input):
        self.update_status("Processing...")
        
        try:
            # If there's an uploaded file
            if hasattr(self, 'uploaded_file'):
                # For images
                if self.uploaded_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = Image.open(self.uploaded_file)
                    
                    # Send image and text to Gemini
                    response = self.vision_model.generate_content([user_input, img])
                else:
                    # For documents, read content (simplified)
                    try:
                        with open(self.uploaded_file, 'r', encoding='utf-8') as f:
                            doc_content = f.read()
                    except UnicodeDecodeError:
                        # Handle binary files
                        doc_content = f"Binary file: {os.path.basename(self.uploaded_file)}"
                    
                    # Send document and text to Gemini
                    response = self.text_model.generate_content([user_input, doc_content])
                
                # Remove the uploaded file after processing
                del self.uploaded_file
            else:
                # Text only
                response = self.text_model.generate_content(user_input)
            
            # Display response
            self.display_message("Gemini", response.text)
            self.update_status("Done")
            
        except Exception as e:
            self.display_message("System", f"Error: {str(e)}")
            self.update_status("Error occurred")
    
    def display_message(self, sender, message):
        self.chat_text.config(state=tk.NORMAL)
        
        # Format message
        if sender == "You":
            tag = "user"
            self.chat_text.insert(tk.END, f"You: ", ("user_tag", "bold"))
        else:
            tag = "bot"
            self.chat_text.insert(tk.END, f"Gemini: ", ("bot_tag", "bold"))
        
        self.chat_text.insert(tk.END, f"{message}\n\n", tag)
        
        # Scroll to bottom
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiChatbot(root)
    
    # Configure chat text styles
    app.chat_text.tag_config("user", foreground="blue")
    app.chat_text.tag_config("bot", foreground="green")
    app.chat_text.tag_config("user_tag", foreground="blue", lmargin1=10, lmargin2=20)
    app.chat_text.tag_config("bot_tag", foreground="green", lmargin1=10, lmargin2=20)
    app.chat_text.tag_config("bold", font=("Helvetica", 12, "bold"))
    
    root.mainloop()