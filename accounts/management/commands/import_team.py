from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import Profile, User

# (name, role_label, TYPE, image file, email, linkedin, github, bio)
MEMBERS = [
    ("Hemant Ojha", "ML-Lead", "LEAD", "Hemant Ojha.png", "2818hemant@gmail.com", "https://www.linkedin.com/in/hemantojha1228/", "https://github.com/SonGoku2818", ""),
    ("Shrey Jaiswal", "Volunteer", "VOLUNTEER", "Shrey.jpg", "5aprilshrey@gmail.com", "https://www.linkedin.com/in/shreyjaiswal1/", "https://github.com/ShreyJaiswal1", ""),
    ("Anupam Yadav", "Volunteer", "VOLUNTEER", "Anupam Yadav.jpg", "anuragyadavanupam@gmail.com", "https://www.linkedin.com/in/anupamyadavanurag", "https://github.com/AnupamYadavAnurag", ""),
    ("Rehan Khan", "Volunteer", "VOLUNTEER", "Rehan Khan.jpg", "khanrehanamir786@gmail.com", "https://www.linkedin.com/in/rehan-khan-8651492a6", "https://github.com/rehanKhan-sudo", ""),
    ("Pushpit Saluja", "AI-Lead", "LEAD", "Pushpit Saluja.jpg", "salujapushpit3@gmail.com", "https://www.linkedin.com/in/pushpit-saluja", "https://github.com/saluja-ji", ""),
    ("Harshit Pandey", "Volunteer", "VOLUNTEER", "Harshit Pandey.jpg", "harshitpandeyy19@gmail.com", "https://www.linkedin.com/in/harshit-pandey-a78929339", "https://github.com/harshitpandeyy19-droid", ""),
    ("Kavaljeet Singh", "Tech-Lead", "LEAD", "KAVALJEET SINGH.jpg", "kavaljeetsingh.dev@gmail.com", "https://www.linkedin.com/in/kavaljeet-singh-dev", "https://github.com/kavaljeetsingh-dev", ""),
    ("Sanya Gupta", "Volunteer", "VOLUNTEER", "Sanya Gupta.jpg", "sanyag788@gmail.com", "https://www.linkedin.com/in/sanyagupta788", "https://github.com/Sanya-gg", ""),
    ("Unnati Kesarwani", "Outreach & Management Lead", "LEAD", "Unnati.png", "unnatikesarwani27@gmail.com", "https://www.linkedin.com/in/unnati-kesarwani-00a131308", "https://github.com/unnatikesarwani", ""),
    ("Tejash Yadav", "Volunteer", "VOLUNTEER", "Tejash Yadav.jpg", "tejashyadavcr7@gmail.com", "https://www.linkedin.com/in/tejash-yadav-307224274/", "https://github.com/tejashxv", ""),
    ("Sejal Kesarwani", "Volunteer", "VOLUNTEER", "Sejal Kesarwani.jpg", "sejalkesarwani23@gmail.com", "https://www.linkedin.com/in/sejal-kesarwani-359891343?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/sejalkesarwani23-code", ""),
    ("Akhilesh Tiwari", "Volunteer", "VOLUNTEER", "Akhilesh Tiwari.jpeg", "10akhil.t@gmail.com", "https://www.linkedin.com/in/akhil-is-dev100", "https://www.github.com/silky-x0", ""),
    ("Saumya Rawat", "Volunteer", "VOLUNTEER", "Saumya Rawat.jpg", "saumya.rawat412@gmail.com", "https://www.linkedin.com/in/saumya-rawat-961a60337?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/Saumya-1995", ""),
    ("Siddharth Singh", "Design & Social Media Lead", "LEAD", "Siddharth Singh.png", "siddharth.wikiclubtech@gmail.com", "https://www.linkedin.com/in/siddharth-singh-6414432b2", "https://github.com/Siddharth-Singh-7", ""),
    ("Vratej Dwivedi", "Volunteer", "VOLUNTEER", "Vratej Dwivedi.png", "vratejdiwedi000@gmail.com", "https://www.linkedin.com/in/vratej-dwivedi-740957286/", "https://github.com/VRATEJDWIVEDI/", ""),
    ("Mohd Shadab", "Envoy", "ENVOY", "Mohd Shadab.jpg", "shadabgdg@gmail.com", "https://www.linkedin.com/in/mohdshadabdev", "https://github.com/mohdshadabdev", ""),
    ("Sanskar Dubey", "Mentor", "MENTOR", "Sanskar Dubey.jpg", "sanskardubeydev@gmail.com", "https://www.linkedin.com/in/sanskardev/", "Dubeysanskar", ""),
    ("Saumya Agrahari", "Volunteer", "VOLUNTEER", "Saumya Agrahari.jpg", "saumyaagrahari262730@gmail.com", "https://www.linkedin.com/in/saumya-agrahari-924900347?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/saumya3005", ""),
    ("Ayush Tiwari", "Volunteer", "VOLUNTEER", "Ayush WikiClubTech-UU.jpg", "ayush.wikiclubtech@gmail.com", "https://www.linkedin.com/in/ayush-tiwari-9601a7348", "https://github.com/ayush26011", ""),
    ("Anshuman Rai", "Co-Envoy", "ENVOY", "Anshuman Rai.jpg", "anshuman.wikiclubtech@gmail.com", "https://www.linkedin.com/in/anshuman-rai-0433032b9/", "", ""),
    ("Ankit Kumar Verma", "Project Coordinator Wiki@IIIT Hyderabad", "COORDINATOR", "ankitsir.png", "ankitkumarverma2003@gmail.com", "https://www.linkedin.com/in/ankit-kumar-verma-081804160", "",
     "Founder of GDG prayagraj, Project Coordinator of Wiki@IIIT Hyderabad, and a passionate tech enthusiast. With a strong background in software development and community building, Ankit has been instrumental in fostering a collaborative environment for tech enthusiasts at IIIT Hyderabad. His dedication to promoting open-source technologies and empowering the next generation of developers has made him a key figure in the tech community. Ankit's vision is to create a thriving ecosystem where knowledge sharing and innovation go hand in hand, driving positive change in the world of technology."),
    ("Shami Verma", "Volunteer", "VOLUNTEER", "Shami verma.jpg", "shamiverma2307@gmail.com", "https://www.linkedin.com/in/shami-v-37195827a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/Shamiverma/internship.git", ""),
    ("Syed Sohrab Haider Rizvi", "Volunteer", "VOLUNTEER", "Sohrab Rizvi.jpg", "sohrab.june17@gmail.com", "https://linkedin.com/in/syed-sohrab-haider-rizvi-589a91385", "https://github.com/StormZShr", ""),
    ("Manvi Keshari", "Volunteer", "VOLUNTEER", "Manvi Keshari.jpg", "manvikeshari06@gmail.com", "https://www.linkedin.com/in/manvi-keshari-287aa2321", "https://github.com/manvikeshari", ""),
    ("Khushi Verma", "Volunteer", "VOLUNTEER", "Khushi Verma.jpg", "khushi753verma@gmail.com", "https://www.linkedin.com/in/khushi-verma-818023322", "https://github.com/khushi0753", ""),
    ("Anuj Kesarwani", "Volunteer", "VOLUNTEER", "Anuj Kesarwani.jpg", "anujkesarwani25@gmail.com", "https://www.linkedin.com/in/anuj-kesarwani-627b3a334?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/anujkesarwani25", ""),
    ("Rishang Mishra", "Volunteer", "VOLUNTEER", "Rishang Mishra.jpeg", "mishrarishang21@gmail.com", "https://www.linkedin.com/in/rishang196", "https://github.com/Rishang196", ""),
    ("Abhinisht Singh", "Volunteer", "VOLUNTEER", "Abhinisht Singh.jpg", "a9793379476@gmail.com", "https://linkedin.com/in/abhinisht-singh-1271ab311", "https://github.com/Abhinisht", ""),
    ("Ashutosh Mishra", "Volunteer", "VOLUNTEER", "Ashutosh Mishra.jpg", "c.t.o.curelex26@gmail.com", "https://www.linkedin.com/in/ashutosh-mishra-841408324", "https://github.com/Ashutosh26-uu", ""),
    ("Sneha Gupta", "Volunteer", "VOLUNTEER", "Sneha Gupta.jpeg", "711snehagupta@gmail.com", "https://www.linkedin.com/in/sneha-gupta-045303318", "https://github.com/711snehagupta", ""),
    ("Prakhar Rai", "Volunteer", "VOLUNTEER", "Prakhar Rai.jpg", "prakharraiuu@gmail.com", "https://www.linkedin.com/in/prakhar-rai-9ab284386?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "https://github.com/prakharraiuu", ""),
    ("Trisha Mishra", "Volunteer", "VOLUNTEER", "Trisha Mishra.jpg", "trishamishra371@gmail.com", "https://www.linkedin.com/in/trisha-mishra-515473316?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", "", ""),
    ("Mahin Farooqui", "Volunteer", "VOLUNTEER", "Mahin Farooqui.jpeg", "farooquimahin30@gmail.com", "www.linkedin.com/in/mahin-farooquiii", "https://github.com/farooquimahin", ""),
]


def clean_url(value, github_prefix=False):
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("http"):
        return value
    if github_prefix and "/" not in value:
        return "https://github.com/" + value
    return "https://" + value


class Command(BaseCommand):
    help = "Purani team list ko database me import karta hai (dobara chalane pe duplicate nahi banta)"

    def add_arguments(self, parser):
        parser.add_argument("images_dir", help="Frontend ke public/team folder ka path")

    def handle(self, *args, **options):
        images_dir = Path(options["images_dir"])
        if not images_dir.exists():
            self.stderr.write(self.style.ERROR(f"Folder nahi mila: {images_dir}"))
            return

        new_users = 0
        for order, (name, label, role_type, image, email, linkedin, github, bio) in enumerate(MEMBERS, start=1):
            name = name.strip().title()
            user = User.objects.filter(email__iexact=email).first()
            if user is None:
                first, _, last = name.partition(" ")
                base = slugify(name) or "member"
                username, n = base, 2
                while User.objects.filter(username=username).exists():
                    username = f"{base}-{n}"
                    n += 1
                user = User(
                    username=username, email=email,
                    first_name=first, last_name=last, role=User.Role.MEMBER,
                )
                user.set_unusable_password()  # login tab milega jab admin password set kare
                user.save()
                new_users += 1

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.member_title = role_type
            profile.role_label = label
            profile.public_email = email
            profile.linkedin = clean_url(linkedin)
            profile.github = clean_url(github, github_prefix=True)
            profile.bio = bio
            profile.show_on_team = True
            profile.display_order = order

            path = images_dir / image
            if image and path.exists():
                if not profile.photo:
                    with open(path, "rb") as f:
                        profile.photo.save(path.name, File(f), save=False)
            elif image:
                self.stdout.write(self.style.WARNING(f"Image nahi mili: {image}"))

            profile.save()

        self.stdout.write(self.style.SUCCESS(f"Done. {new_users} naye users bane, {len(MEMBERS)} profiles update hue."))