from datetime import datetime
from pathlib import Path

import frontmatter
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from blogs.models import Blog


def find_or_create_author(name):
    """Author ka naam kisi team member se match ho to wahi user, warna naya bana do."""
    name = (name or "WikiClub Tech UU").strip()
    for user in User.objects.all():
        if user.get_full_name().strip().lower() == name.lower():
            return user

    base = slugify(name) or "wikiclub"
    username, n = base, 2
    while User.objects.filter(username=username).exists():
        username = f"{base}-{n}"
        n += 1
    first, _, last = name.partition(" ")
    user = User(
        username=username,
        email=f"{username}@wikiclub.local",
        first_name=first,
        last_name=last,
        role=User.Role.MEMBER,
    )
    user.set_unusable_password()
    user.save()
    return user


class Command(BaseCommand):
    help = "Frontend ke src/data/blogs ke .md blogs ko database me import karta hai"

    def add_arguments(self, parser):
        parser.add_argument("blogs_dir", help="Frontend ke src/data/blogs folder ka path")

    def handle(self, *args, **options):
        folder = Path(options["blogs_dir"])
        if not folder.exists():
            self.stderr.write(self.style.ERROR(f"Folder nahi mila: {folder}"))
            return

        count = 0
        for md in sorted(folder.glob("*.md")):
            post = frontmatter.loads(md.read_text(encoding="utf-8"))
            meta = post.metadata

            raw_date = str(meta.get("date", ""))[:10]
            try:
                published = timezone.make_aware(datetime.strptime(raw_date, "%Y-%m-%d"))
            except ValueError:
                published = timezone.now()

            Blog.objects.update_or_create(
                slug=md.stem,
                defaults={
                    "title": meta.get("title", md.stem),
                    "excerpt": meta.get("excerpt", ""),
                    "content": post.content,
                    "cover_image_url": meta.get("image", ""),
                    "tags": list(meta.get("tags", [])),
                    "status": Blog.Status.PUBLISHED,
                    "published_at": published,
                    "author": find_or_create_author(meta.get("author")),
                },
            )
            count += 1
            self.stdout.write(f"Imported: {md.name}")

        self.stdout.write(self.style.SUCCESS(f"Done. {count} blogs import hue."))