from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
import qrcode

from .models import Book, Member, IssueBook
from .serializers import BookSerializer, MemberSerializer, IssueBookSerializer


# =========================
# API VIEWSETS
# =========================

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class IssueBookViewSet(viewsets.ModelViewSet):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer


# =========================
# DASHBOARD
# =========================

def dashboard(request):
    return render(request, "dashboard.html", {
        "books": Book.objects.count(),
        "members": Member.objects.count(),
        "issued": IssueBook.objects.count(),
    })


# =========================
# BOOKS
# =========================

def book_list(request):
    return render(request, "books.html", {
        "books": Book.objects.all()
    })


def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            title=request.POST.get("title"),
            author=request.POST.get("author"),
            isbn=request.POST.get("isbn"),
            quantity=int(request.POST.get("quantity") or 1)
        )
        return redirect("books-page")

    return render(request, "add_book.html")


def edit_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.isbn = request.POST.get("isbn")
        book.quantity = int(request.POST.get("quantity") or 1)
        book.save()
        return redirect("books-page")

    return render(request, "edit_book.html", {"book": book})


def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect("books-page")


# =========================
# MEMBERS
# =========================

def member_list(request):
    return render(request, "members.html", {
        "members": Member.objects.all()
    })


def add_member(request):
    if request.method == "POST":
        Member.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone")
        )
        return redirect("members-page")

    return render(request, "add_member.html")


def edit_member(request, id):
    member = get_object_or_404(Member, id=id)

    if request.method == "POST":
        member.name = request.POST.get("name")
        member.email = request.POST.get("email")
        member.phone = request.POST.get("phone")
        member.save()
        return redirect("members-page")

    return render(request, "edit_member.html", {"member": member})


def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    member.delete()
    return redirect("members-page")


# =========================
# ISSUE BOOKS
# =========================

def issue_book_list(request):
    return render(request, "issue_books.html", {
        "issued_books": IssueBook.objects.all()
    })


def issue_book(request):
    if request.method == "POST":
        book = get_object_or_404(Book, id=request.POST.get("book"))
        member = get_object_or_404(Member, id=request.POST.get("member"))

        IssueBook.objects.create(book=book, member=member)

        return redirect("issue-books-page")

    return render(request, "issue_book.html", {
        "books": Book.objects.all(),
        "members": Member.objects.all()
    })


# =========================
# RETURN BOOK
# =========================

def return_book(request, id):
    issue = get_object_or_404(IssueBook, id=id)

    if not issue.return_date:
        issue.return_date = timezone.now().date()

    issue.save()
    return redirect("issue-books-page")


# =========================
# QR CODE
# =========================

def generate_qr(request, id):
    book = get_object_or_404(Book, id=id)

    qr = qrcode.make(f"BOOK-{book.id}-{book.title}")

    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")

    return response