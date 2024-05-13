import json
import sys

import jwt
import pyperclip
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, TextArea


class JwtTui(App):
    TITLE = "JwtTui"
    TOKEN = ""
    PAYLOAD = ""
    HEADERS = ""
    CSS_PATH = "style.css"
    BINDINGS = [("escape", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Label("Token"),
            Input(placeholder="Token input", id="input"),
            Label("Headers"),
            TextArea.code_editor(self.HEADERS, language="json", id="headers"),
            Label("Payload"),
            TextArea.code_editor(self.PAYLOAD, language="json", id="payload"),
            Horizontal(
                Button("Clear", id="clear"),
                Button("Copy Payload", id="copy_payload"),
                Button("Copy Headers", id="copy_headers"),
                Button("Quit", id="quit"),
                id="buttons",
            ),
            id="main",
        )
        yield Footer()

    def on_mount(self):
        arguments = sys.argv
        if len(arguments) > 1:
            self.TOKEN = arguments[1]
            obj1 = self.query_one("#input")
            obj1.value = self.TOKEN

    @on(Input.Changed)
    def decode(self, value):
        text = value.value
        try:
            decoded = jwt.decode(text, options={"verify_signature": False})
            headers = jwt.get_unverified_header(text)
            self.PAYLOAD = decoded
            parsed_payload = json.dumps(decoded, indent=4)
            parsed_headers = json.dumps(headers, indent=4)
            obj1 = self.query_one("#payload")
            obj1.text = parsed_payload
            obj2 = self.query_one("#headers")
            obj2.text = parsed_headers
        except Exception:
            obj1 = self.query_one("#payload")
            obj1.text = "Invalid token"

    def on_button_pressed(self, event):
        id = str(event.button.id).strip()
        if id == "clear":
            obj1 = self.query_one("#input")
            obj1.value = ""
            obj2 = self.query_one("#payload")
            obj2.text = ""
            obj3 = self.query_one("#headers")
            obj3.text = ""
            obj1.focus()
        elif id == "copy_payload":
            obj1 = self.query_one("#payload")
            pyperclip.copy(obj1.text)
        elif id == "copy_headers":
            obj1 = self.query_one("#headers")
            pyperclip.copy(obj1.text)
        elif id == "quit":
            self.quit()

    def quit(self):
        sys.exit()


if __name__ == "__main__":
    app = JwtTui()
    app.run()
