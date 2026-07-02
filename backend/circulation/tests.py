from django.test import TestCase

from catalog.models import Book, BookCopy
from members.models import Member, Membership

from .services import CirculationError, checkout


class CheckoutLoanLimitTests(TestCase):
    def setUp(self):
        self.membership = Membership.objects.create(
            type_name="Standard", loan_limit=1, loan_duration_days=14
        )
        self.member = Member.objects.create(
            name="Test Member", email="test.member@example.com", membership=self.membership
        )
        self.book = Book.objects.create(isbn="000-0-00-000000-0", title="Test Book")
        self.copy1 = BookCopy.objects.create(book=self.book, barcode="TEST-01")
        self.copy2 = BookCopy.objects.create(book=self.book, barcode="TEST-02")

    def test_checkout_blocked_when_loan_limit_reached(self):
        checkout(self.member, self.copy1)

        with self.assertRaises(CirculationError):
            checkout(self.member, self.copy2)
