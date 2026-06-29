"""Populate the database with realistic sample data for demos and testing.

Run with:  python manage.py seed_data
"""
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Author, Category, Book, BookCopy
from members.models import Membership, Member, Staff
from circulation.models import Loan
from reservations.models import Reservation
from reporting.services import issue_overdue_fine


class Command(BaseCommand):
    help = "Seed the database with sample library data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # --- Users -------------------------------------------------------
        admin, created = User.objects.get_or_create(
            username="admin", defaults={"is_staff": True, "is_superuser": True, "email": "admin@lib.test"}
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        lib_user, created = User.objects.get_or_create(
            username="librarian", defaults={"is_staff": True, "email": "lib@lib.test"}
        )
        if created:
            lib_user.set_password("library123")
            lib_user.save()

        staff, _ = Staff.objects.get_or_create(
            user=lib_user,
            defaults={"name": "Aisha Rahman", "email": "lib@lib.test", "role": Staff.Role.LIBRARIAN},
        )

        # --- Memberships -------------------------------------------------
        standard, _ = Membership.objects.get_or_create(
            type_name="Standard",
            defaults={"loan_limit": 3, "loan_duration_days": 14, "can_reserve": True},
        )
        premium, _ = Membership.objects.get_or_create(
            type_name="Premium",
            defaults={"loan_limit": 10, "loan_duration_days": 30, "can_reserve": True},
        )
        student, _ = Membership.objects.get_or_create(
            type_name="Student",
            defaults={"loan_limit": 5, "loan_duration_days": 21, "can_reserve": True},
        )

        # --- Members -----------------------------------------------------
        members_data = [
            ("Lim Wei", "wei@mail.test", standard),
            ("Nurul Huda", "nurul@mail.test", student),
            ("Raj Kumar", "raj@mail.test", premium),
            ("Siti Aminah", "siti@mail.test", standard),
        ]
        members = []
        for name, email, ms in members_data:
            m, _ = Member.objects.get_or_create(
                email=email, defaults={"name": name, "membership": ms}
            )
            members.append(m)

        # --- Authors & Categories ---------------------------------------
        authors = {}
        for a in ["Robert C. Martin", "Erich Gamma", "Martin Fowler", "Kent Beck", "Andrew Hunt"]:
            authors[a], _ = Author.objects.get_or_create(name=a)

        cats = {}
        for c in ["Software Engineering", "Design Patterns", "Agile", "Programming"]:
            cats[c], _ = Category.objects.get_or_create(name=c)

        # --- Books & Copies ---------------------------------------------
        books_data = [
            ("978-0132350884", "Clean Code", ["Robert C. Martin"], ["Software Engineering", "Programming"], 3),
            ("978-0201633610", "Design Patterns", ["Erich Gamma"], ["Design Patterns"], 2),
            ("978-0201485677", "Refactoring", ["Martin Fowler"], ["Software Engineering"], 2),
            ("978-0321146533", "Test-Driven Development", ["Kent Beck"], ["Agile", "Programming"], 1),
            ("978-0135957059", "The Pragmatic Programmer", ["Andrew Hunt"], ["Programming"], 2),
            ("978-0134494166", "Clean Architecture", ["Robert C. Martin"], ["Software Engineering"], 1),
        ]
        books = []
        for isbn, title, author_names, cat_names, copy_count in books_data:
            book, created = Book.objects.get_or_create(
                isbn=isbn, defaults={"title": title, "publisher": "Tech Press", "publication_year": 2018}
            )
            if created:
                book.authors.set([authors[n] for n in author_names])
                book.categories.set([cats[n] for n in cat_names])
                for i in range(copy_count):
                    BookCopy.objects.create(
                        book=book, barcode=f"{isbn[-4:]}-{i+1:02d}", shelf_location=f"A{len(books)+1}"
                    )
            books.append(book)

        # --- A normal active loan ---------------------------------------
        copy = books[0].copies.filter(status=BookCopy.Status.AVAILABLE).first()
        if copy and not Loan.objects.filter(member=members[0], status=Loan.Status.ACTIVE).exists():
            Loan.objects.create(
                copy=copy, member=members[0], staff=staff,
                due_date=timezone.now().date() + timedelta(days=14),
            )
            copy.mark_on_loan()

        # --- An overdue loan that generates a fine on return -------------
        copy2 = books[1].copies.filter(status=BookCopy.Status.AVAILABLE).first()
        if copy2 and not Loan.objects.filter(member=members[1], status=Loan.Status.ACTIVE).exists():
            overdue = Loan.objects.create(
                copy=copy2, member=members[1], staff=staff,
                due_date=timezone.now().date() - timedelta(days=5),
            )
            copy2.mark_on_loan()
            # Demonstrate the fine pathway directly:
            overdue.return_date = timezone.now().date()
            overdue.status = Loan.Status.RETURNED
            overdue.save()
            copy2.mark_available()
            issue_overdue_fine(overdue)

        # --- A reservation on a fully-loaned title -----------------------
        Reservation.objects.get_or_create(book=books[3], member=members[2])

        self.stdout.write(self.style.SUCCESS("Done. Logins: admin/admin123, librarian/library123"))
