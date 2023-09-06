import argparse
import json
import os

import more_itertools
from jinja2 import Environment, FileSystemLoader
from livereload import Server, shell

FILEPATH = "data.json"


def on_reload():
    with open(FILEPATH, encoding="utf-8") as json_file:
        books = json.load(json_file)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(
        "templates/index.html",
    )
    books_per_page = 10
    book_chunks = list(more_itertools.chunked(books, books_per_page))
    page_count = len(book_chunks)
    for page_number, book_list in enumerate(book_chunks, 1):
        os.makedirs("pages", exist_ok=True)
        file_path = os.path.join("pages", f"index{page_number}.html")
        current_page = page_number
        rendered_html = template.render(
      
            books=book_list,
            page_count=page_count,
            current_page=current_page,
        )
        with open(file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_html)


def main():
    on_reload()
    server = Server()
    server.watch("templates/*.html", on_reload)
    server.serve()


if __name__ == "__main__":
    main()
