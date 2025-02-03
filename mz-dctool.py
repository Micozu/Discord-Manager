import tkinter as tk
import customtkinter as ctk
import requests
import threading
import webbrowser
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
import re

# Create a ThreadPoolExecutor to manage threads efficiently
executor = ThreadPoolExecutor(max_workers=4)

# Function to send a single webhook message
def send_message(app, webhook_url, message):
    app.update_status("Sending message...", "yellow")
    try:
        # Validate URL format
        if not validate_url(webhook_url):
            app.update_status("Invalid webhook URL.", "red")
            return

        data = {'content': message}
        response = requests.post(webhook_url, json=data, timeout=5)  # Set timeout
        if response.status_code == 204:
            app.update_status("Message sent successfully.", "green")
        else:
            app.update_status(f"Failed to send message: {response.status_code}", "red")
    except requests.Timeout:
        app.update_status("Request timed out. Please try again.", "red")
    except requests.RequestException as e:
        app.update_status(f"Request error: {e}", "red")


# Function to send multiple messages (rapid send)
def rapid_send(app, webhook_url, message, count):
    app.update_status(f"Sending {count} messages...", "yellow")
    for i in range(count):
        send_message(app, webhook_url, message)
        app.update_progress(i + 1, count)  # Update progress bar
    app.update_status(f"Successfully sent {count} messages.", "green")


# Function to delete the webhook
def delete_webhook(app, webhook_url):
    app.update_status("Deleting webhook...", "yellow")
    try:
        # Validate URL format
        if not validate_url(webhook_url):
            app.update_status("Invalid webhook URL.", "red")
            return

        response = requests.delete(webhook_url, timeout=5)  # Set timeout
        if response.status_code == 204:
            app.update_status("Webhook deleted successfully.", "green")
        else:
            app.update_status(f"Failed to delete webhook: {response.status_code}", "red")
    except requests.Timeout:
        app.update_status("Request timed out. Please try again.", "red")
    except requests.RequestException as e:
        app.update_status(f"Request error: {e}", "red")


# Function to fetch webhook info
def get_webhook_info(app, webhook_url):
    app.update_status("Fetching webhook info...", "yellow")
    try:
        # Validate URL format
        if not validate_url(webhook_url):
            app.update_status("Invalid webhook URL.", "red")
            return

        response = requests.get(webhook_url, timeout=5)  # Set timeout
        if response.status_code == 200:
            info = response.json()
            app.update_status(f"Webhook info: {info['name']} - {info['avatar']}", "green")
        else:
            app.update_status(f"Failed to fetch info: {response.status_code}", "red")
    except requests.Timeout:
        app.update_status("Request timed out. Please try again.", "red")
    except requests.RequestException as e:
        app.update_status(f"Request error: {e}", "red")


# Function to protect webhook from deletion
def protect_webhook(app, webhook_url):
    app.update_status("Protecting webhook...", "yellow")
    try:
        # Validate URL format
        if not validate_url(webhook_url):
            app.update_status("Invalid webhook URL.", "red")
            return

        headers = {'X-Webhook-Protection': 'enabled'}
        response = requests.patch(webhook_url, headers=headers, timeout=5)  # Set timeout
        if response.status_code == 200:
            app.update_status("Webhook protection enabled.", "green")
        else:
            app.update_status(f"Failed to protect webhook: {response.status_code}", "red")
    except requests.Timeout:
        app.update_status("Request timed out. Please try again.", "red")
    except requests.RequestException as e:
        app.update_status(f"Request error: {e}", "red")


# Function to open Discord invite
def open_discord():
    try:
        webbrowser.open('https://discord.gg/mJmFQDJ5W8')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Discord invite: {e}")


# Function to run tasks in a separate thread to avoid blocking the UI
def run_task(app, func, *args):
    executor.submit(func, app, *args)


# Validate Webhook URL (Simple Regex for URL validation)
def validate_url(url):
    pattern = r"^https://discord.com/api/webhooks/\d+/[a-zA-Z0-9_-]+$"
    return re.match(pattern, url) is not None


# Main application UI
class WebhookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Discord Webhook Manager")
        self.geometry("800x500")
        self.configure(bg="#2C2C2C")

        # Set custom blue theme (default theme)
        ctk.set_appearance_mode("dark")  # dark mode
        ctk.set_default_color_theme("blue")  # default blue theme

        # Header
        header = ctk.CTkLabel(self, text="Discord Webhook Manager", font=("Arial", 24, "bold"), text_color="white")
        header.grid(row=0, column=0, columnspan=2, pady=20)

        # Webhook URL Input
        self.webhook_url_label = ctk.CTkLabel(self, text="Webhook URL:", text_color="white")
        self.webhook_url_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.webhook_url_entry = ctk.CTkEntry(self, placeholder_text="Enter Webhook URL")
        self.webhook_url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Message Input
        self.message_label = ctk.CTkLabel(self, text="Message to Send:", text_color="white")
        self.message_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.message_entry = ctk.CTkEntry(self, placeholder_text="Enter message")
        self.message_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Buttons
        self.send_button = ctk.CTkButton(self, text="Send Message", command=self.send_message)
        self.send_button.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.rapid_send_button = ctk.CTkButton(self, text="Rapid Send", command=self.rapid_send_message)
        self.rapid_send_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        self.delete_button = ctk.CTkButton(self, text="Delete Webhook", command=self.delete_webhook)
        self.delete_button.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        self.protect_button = ctk.CTkButton(self, text="Protect Webhook", command=self.protect_webhook)
        self.protect_button.grid(row=4, column=1, pady=10, padx=10, sticky="ew")

        self.get_info_button = ctk.CTkButton(self, text="Get Webhook Info", command=self.get_webhook_info)
        self.get_info_button.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=6, column=0, columnspan=2, pady=20)
        self.progress_bar.set(0)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Waiting for action...", font=("Arial", 12), text_color="white")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=10)

        # Footer
        footer = ctk.CTkLabel(self, text="Created by Micozu", font=("Arial", 10), text_color="white")
        footer.grid(row=8, column=0, columnspan=2, pady=10)

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_status(self, text, color):
        """ Update the status label with the given text and color. """
        self.status_label.configure(text=text, text_color=color)

    def update_progress(self, current, total):
        """ Update the progress bar safely in the main thread. """
        progress = current / total
        self.progress_bar.set(progress)

    def send_message(self):
        webhook_url = self.webhook_url_entry.get()
        message = self.message_entry.get()
        if webhook_url and message:
            run_task(self, send_message, webhook_url, message)
        else:
            self.update_status("Please enter both Webhook URL and message.", "red")

    def rapid_send_message(self):
        webhook_url = self.webhook_url_entry.get()
        message = self.message_entry.get()
        if webhook_url and message:
            count = 69  # Example: send 69 messages rapidly
            run_task(self, rapid_send, webhook_url, message, count)
        else:
            self.update_status("Please enter both Webhook URL and message.", "red")

    def delete_webhook(self):
        webhook_url = self.webhook_url_entry.get()
        run_task(self, delete_webhook, webhook_url)

    def protect_webhook(self):
        webhook_url = self.webhook_url_entry.get()
        run_task(self, protect_webhook, webhook_url)

    def get_webhook_info(self):
        webhook_url = self.webhook_url_entry.get()
        run_task(self, get_webhook_info, webhook_url)


if __name__ == "__main__":
    app = WebhookApp()
    app.mainloop()
