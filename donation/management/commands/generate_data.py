import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from tqdm import tqdm

from cause.models import Cause
from donation.models import Donation
from users.models import Profile


class Command(BaseCommand):
    help = "Generate dummy data for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate 1000 users with profiles
        self.stdout.write("Generating 1000 users...")
        users = []
        for i in tqdm(range(1000), desc="Users"):
            username = fake.user_name()
            email = fake.email()
            user = User(username=username+str(i), email=email)
            user.set_password("password")
            users.append(user)
        User.objects.bulk_create(users)
        self.stdout.write("1000 users created.")

        # Create profiles for the users
        self.stdout.write("Generating profiles for users...")
        profiles = [
            Profile(user=user, phone=fake.phone_number()[:15])
            for user in tqdm(users, desc="Profiles")
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write("Profiles created.")

        # Generate 500 causes
        self.stdout.write("Generating 500 causes...")
        causes = []
        for _ in tqdm(range(500), desc="Causes"):
            name = fake.catch_phrase()
            tagline = fake.sentence(nb_words=6)
            description = fake.text(max_nb_chars=200)
            end_date = datetime.now() + timedelta(days=random.randint(30, 365))
            cause = Cause(
                name=name, tagline=tagline, description=description, end_date=end_date
            )
            causes.append(cause)
        Cause.objects.bulk_create(causes)
        self.stdout.write("500 causes created.")

        # Generate 10,000 donations
        self.stdout.write("Generating 10,000 donations...")
        donations = []
        users = list(User.objects.all())
        causes = list(Cause.objects.all())
        for _ in tqdm(range(10000), desc="Donations"):
            donor = random.choice(users)
            cause = random.choice(causes)
            amount = round(random.uniform(10.0, 10000.0), 2)
            donation = Donation(donor=donor, amount=amount, cause=cause)
            donations.append(donation)
        Donation.objects.bulk_create(donations)
        self.stdout.write("10,000 donations created.")

        self.stdout.write("Data generation complete.")
