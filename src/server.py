import http.server
import os
import socketserver

PORT = 8000

# Типы контента по расширению файла
content_types = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

# Базовая директория скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ContactPageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # По умолчанию загружается index.html
        rel_path = self.path[1:] or "index.html"
        ext = os.path.splitext(rel_path)[1]
        content_type = content_types.get(ext, "text/plain")

        abs_path = os.path.join(BASE_DIR, rel_path)

        try:
            with open(abs_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, f"Файл {rel_path} не найден.")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ContactPageHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")
