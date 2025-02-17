import json
import logging
from pathlib import Path
from jinja2 import Template

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LinkNetGen:
    def __init__(self) -> None:
        self.template_path = Path(__file__).parent / "template" / "index.html"
        self.config_path = Path(__file__).parent / "config.json"
        self.template = Template("")
        self.data = {}
        self.doc = ""

    def load_file(self, file_path: Path, default_content: str = "") -> str:
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            return default_content
        except Exception as e:
            logging.error(f"Failed to load file: {e}")
            return default_content

    def add_template(self):
        template_content = self.load_file(self.template_path)
        self.template = Template(template_content)
        logging.info("Template loaded successfully.")

    def add_config(self):
        config_content = self.load_file(self.config_path, "{}")
        try:
            self.data = json.loads(config_content)
            self.items_per_page = self.data.get("items_per_page", 10)
            logging.info("Configuration loaded successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON config: {e}")
            self.data = {}

    def gen_str(self):
        try:
            links = self.data.get("links", {})
            paginated_data = [
                links.items()[i:i + self.items_per_page]
                for i in range(0, len(links), self.items_per_page)
            ]
            self.data.update({
                "paginated_links": paginated_data,
                "total_pages": len(paginated_data)
            })
            self.doc = self.template.render(**self.data)
            logging.info("Template rendered successfully.")
        except Exception as e:
            logging.error(f"Failed to render template: {e}")
            self.doc = ""

    def gen_file(self):
        try:
            output_path = Path(__file__).parent / "site" / "index.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, mode="w+", encoding="utf-8") as f:
                f.write(self.doc)
            logging.info("File written successfully.")
        except Exception as e:
            logging.error(f"Failed to write file: {e}")

    def main(self):
        self.add_template()
        self.add_config()
        self.gen_str()
        self.gen_file()

if __name__ == "__main__":
    l1 = LinkNetGen()
    l1.main()
