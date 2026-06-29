"""Catalog Management component models: books, authors, categories, copies."""
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    """A bibliographic record (the title), separate from its physical copies."""
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=300)
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books", blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def available_copies(self):
        return self.copies.filter(status=BookCopy.Status.AVAILABLE).count()

    @property
    def total_copies(self):
        return self.copies.count()


class BookCopy(models.Model):
    """One physical copy of a Book."""
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ON_LOAN = "ON_LOAN", "On loan"
        RESERVED = "RESERVED", "Reserved"
        LOST = "LOST", "Lost"
        DAMAGED = "DAMAGED", "Damaged"

    book = models.ForeignKey(Book, related_name="copies", on_delete=models.CASCADE)
    barcode = models.CharField(max_length=50, unique=True)
    shelf_location = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    acquired_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Book copies"

    def __str__(self):
        return f"{self.book.title} [{self.barcode}]"

    def mark_on_loan(self):
        self.status = self.Status.ON_LOAN
        self.save(update_fields=["status"])

    def mark_available(self):
        self.status = self.Status.AVAILABLE
        self.save(update_fields=["status"])
