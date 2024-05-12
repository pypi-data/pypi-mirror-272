import json
import codecs
import shutil
from pathlib import Path
from dataclasses import dataclass
import markdown
from jinja2 import Environment, FileSystemLoader


def initialize(dest_: Path) -> None:
    assert isinstance(dest_, Path)
    assert dest_.exists()

    shutil.copyfile(
        Path(Path(__file__).resolve().parent, "share", "configs.json"),
        Path(dest_, "configs.json"),
    )


@dataclass
class Menu:
    header: dict
    footer: dict


@dataclass
class Folders:
    output: str
    content: str
    meetups: str
    pages: str


@dataclass
class Configs:
    name: str
    URL: str
    language: str
    theme: str
    title: str
    author: str
    email: str
    description: str
    sitemap: bool
    feeds: bool
    robots: bool
    logo: str
    favicon: str
    copyright: str
    home: str
    folders: dict
    menu: Menu

    @classmethod
    def from_json(cls, json_file: Path):
        assert isinstance(json_file, Path)
        assert json_file.exists()

        with codecs.open(json_file, "r", encoding="utf-8") as f:
            cfgs = json.load(f)
            return cls(
                name=cfgs["name"],
                URL=cfgs["URL"],
                language=cfgs["language"],
                theme=cfgs["theme"],
                title=cfgs["title"],
                author=cfgs["author"],
                email=cfgs["email"],
                description=cfgs["description"],
                sitemap=cfgs["sitemap"],
                feeds=cfgs["feeds"],
                robots=cfgs["robots"],
                logo=cfgs["logo"],
                favicon=cfgs["favicon"],
                copyright=cfgs["copyright"],
                home=cfgs["home"],
                folders=Folders(**cfgs["folders"]),
                menu=Menu(**cfgs["menu"]),
            )


@dataclass
class Page:
    """Page Markdown file"""

    title: float
    date: int
    author: str
    slug: str
    status: str
    description: str
    content: str

    @classmethod
    def from_markdown(cls, meetup):
        _md = markdown.Markdown(extensions=["meta", "attr_list"])
        with codecs.open(meetup, "r", encoding="utf-8") as f:
            data = f.read()
            return cls(
                content=_md.convert(data),
                date="".join(_md.Meta["date"]),
                author="".join(_md.Meta["author"]),
                title="".join(_md.Meta["title"]),
                description="".join(_md.Meta["description"]),
                slug="".join(_md.Meta["slug"]),
                status="".join(_md.Meta["status"]),
            )


@dataclass
class Meetup:
    """Meetup Markdown file"""

    id: str
    title: float
    date: int
    author: str
    slug: str
    status: str
    featureimage: str
    address: str
    description: str
    content: str

    @classmethod
    def from_markdown(cls, meetup):
        _md = markdown.Markdown(extensions=["meta", "attr_list"])
        with codecs.open(meetup, "r", encoding="utf-8") as f:
            data = f.read()
            return cls(
                content=_md.convert(data),
                id="".join(_md.Meta["id"]),
                date="".join(_md.Meta["date"]),
                author="".join(_md.Meta["author"]),
                title="".join(_md.Meta["title"]),
                description="".join(_md.Meta["description"]),
                slug="".join(_md.Meta["slug"]),
                featureimage="".join(_md.Meta["featureimage"]),
                address="".join(_md.Meta["address"]),
                status="".join(_md.Meta["status"]),
            )


class Meetlify:
    def __init__(self, dest_: Path) -> None:
        assert isinstance(dest_, Path)

        self._dest = dest_
        self._src = Path(__file__).resolve().parent
        self._configs = Configs.from_json(Path(self._dest, "configs.json"))

        self._render_environment = Environment(
            loader=FileSystemLoader(
                Path(self._dest, "themes", self._configs.theme, "templates")
            )
        )
        self._meetups = []

    def setup(self) -> None:
        Path(self._dest, self._configs.folders.output).mkdir(
            parents=True, exist_ok=True
        )

        # TODO: Support to update themes folder - switch between multiple folders
        shutil.copytree(
            Path(self._src, "themes", self._configs.theme),
            Path(self._dest, "themes", self._configs.theme),
            dirs_exist_ok=True,
        )

        shutil.copytree(
            Path(self._src, "share", "content"),
            Path(self._dest, self._configs.folders.content),
            dirs_exist_ok=True,
        )

    def clean(self):
        output_folder = Path(self._dest, self._configs.folders.output)

        if not output_folder.exists():
            output_folder.mkdir()
        else:
            for path in output_folder.iterdir():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)

    def make(self):
        # Parse all Meetup events available as Markdown
        self._meetups = [
            Meetup.from_markdown(mt)
            for mt in Path(
                self._dest, self._configs.folders.content, "meetups"
            ).iterdir()
            if mt.is_file() and mt.suffix == ".md"
        ]
        self._meetups = sorted(self._meetups, key=lambda x: x.id, reverse=True)

        with codecs.open(
            Path(
                self._dest,
                self._configs.folders.content,
                self._configs.folders.pages,
                f"{self._configs.home}.md",
            ),
            "r",
            encoding="utf-8",
        ) as f:
            data = f.read()
            home_content = markdown.Markdown(extensions=["meta", "attr_list"]).convert(
                data
            )

        with open(
            Path(self._dest, self._configs.folders.output, "index.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self._render_environment.get_template("index.html").render(
                    meta=self._configs,
                    home_content="".join(home_content),
                    meetups=self._meetups[0:3],
                )
            )
            print("... wrote output/home")

        for current_page in ["privacy", "terms", "contact"]:
            page_content = Page.from_markdown(
                Path(
                    self._dest,
                    self._configs.folders.content,
                    "pages",
                    f"{current_page}.md",
                )
            )

            Path(self._dest, self._configs.folders.output, current_page).mkdir(
                parents=True, exist_ok=True
            )

            with open(
                Path(
                    self._dest, self._configs.folders.output, current_page, "index.html"
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self._render_environment.get_template("page.html").render(
                        meta=self._configs, front=page_content
                    )
                )
                print(f"... wrote output/{current_page}")

        # TODO: Check if there are less than 3 meetups and runs without error? make 3 config variable
        with open(
            Path(self._dest, self._configs.folders.output, "404.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self._render_environment.get_template("404.html").render(
                    meta=self._configs, meetups=self._meetups[0:3]
                )
            )
            print("... wrote output/404")

        for current_meetup in self._meetups:
            Path(
                self._dest, self._configs.folders.output, "meetups", current_meetup.slug
            ).mkdir(parents=True, exist_ok=True)

            with open(
                Path(
                    self._dest,
                    self._configs.folders.output,
                    "meetups",
                    current_meetup.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self._render_environment.get_template("meetup.html").render(
                        meta=self._configs,
                        content=current_meetup.content,
                        front=current_meetup,
                    )
                )
                print(f"... wrote output/meetups/{current_meetup.slug}")

        with open(
            Path(self._dest, self._configs.folders.output, "meetups", "index.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self._render_environment.get_template("meetups.html").render(
                    meta=self._configs, meetups=self._meetups
                )
            )
            print("... wrote output/meetups")

        shutil.copytree(
            Path(self._src, "themes", self._configs.theme, "static"),
            Path(
                self._dest,
                self._configs.folders.output,
                "static",
            ),
            dirs_exist_ok=True,
        )
        print("... copied output/themes static folder")

        shutil.copytree(
            Path(self._dest, self._configs.folders.content, "images"),
            Path(
                self._dest,
                self._configs.folders.output,
                "images",
            ),
            dirs_exist_ok=True,
        )
        print("... copied output/images folder")

        if self._configs.robots:
            shutil.copyfile(
                Path(self._src, "share", "robots.txt"),
                Path(
                    self._dest,
                    self._configs.folders.output,
                    "robots.txt",
                ),
            )
            print("... copied output/robots.txt filed")
