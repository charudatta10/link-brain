import json
import logging
from pathlib import Path
from jinja2 import Template

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
)


class LinkNetGen:
    """
    Inputs: template files, config file both located in parent folder
    if file location is different change file location using object instance
    Outputs: site/index.html is generated in parent folder

    """

    def __init__(self) -> None:
        self.template_path = Path(__file__).parent / "template"
        self.config_path = Path(__file__).parent
        self.template = Template("")
        self.data = {}
        self.doc = {}

    def add_template(self):
        try:
            with open(
                self.template_path / "index.html", mode="r", encoding="utf-8"
            ) as template_file:
                template_content = template_file.read()
            self.template = Template(template_content)
            logging.info("Template loaded successfully.")
        except FileNotFoundError as e:
            logging.error(f"Template file not found: {e}")
            self.template = Template("")
        except Exception as e:
            logging.error(f"Failed to load template: {e}")
            self.template = Template("")

    def add_config(self):
        try:
            with open(
                self.config_path / "config.json", mode="r", encoding="utf-8"
            ) as config_file:
                self.data = json.load(config_file)
            self.items_per_page = self.data.get(
                "items_per_page", 10
            )  # Default to 5 items per page
            logging.info("Configuration loaded successfully.")
        except FileNotFoundError as e:
            logging.error(f"Config file not found: {e}")
            self.data = {}
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON config: {e}")
            self.data = {}
        except Exception as e:
            logging.error(f"Failed to load config: {e}")

    def gen_str(self):
        try:
            links = self.data.get("links", {})
            logging.info(f"Links: {links}")
            logging.info(f"Items per page: {self.items_per_page}")
            # Convert the dictionary to a list of tuples
            links_list = list(links.items())
            paginated_data = []
            for i in range(0, len(links_list), self.items_per_page):
                logging.info(f"Slicing from {i} to {i + self.items_per_page}")
                paginated_data.append(links_list[i : i + self.items_per_page])
            logging.info(f"Paginated data: {paginated_data}")
            self.data["paginated_links"] = paginated_data
            self.data["total_pages"] = len(paginated_data)
            self.doc = self.template.render(**self.data)
            logging.info("Template rendered successfully.")
        except Exception as e:
            logging.error(f"Failed to render template: {e}")
            self.doc = ""

    def gen_file(self):
        try:
            output_path = Path(__file__).parent / "site/index.html"
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
