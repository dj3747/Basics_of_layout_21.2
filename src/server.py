import http.server
import os
import socketserver

PORT = 8000
HTML_FILE = os.path.join(os.path.dirname(__file__), "contacts.html")


class ContactPageHandler(http.server.BaseHTTPRequestHandler):
    def do_get(self) -> None:
        try:
            with open(HTML_FILE, "r", encoding="utf-8") as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(500, "HTML файл не найден")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ContactPageHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")
