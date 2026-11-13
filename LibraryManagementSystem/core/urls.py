from django.urls import path
from .views import (
    dashboard,
    book_list,
    add_book,
    edit_book,
    delete_book,
    member_list,
    add_member,
    edit_member,
    delete_member,
    issue_book_list,
    issue_book,
    return_book,
    generate_qr,
)

urlpatterns = [
    # =========================
    # DASHBOARD
    # =========================
    path('', dashboard, name='dashboard'),

    # =========================
    # BOOKS
    # =========================
    path('books/', book_list, name='books-page'),
    path('books/add/', add_book, name='add-book'),
    path('books/edit/<int:id>/', edit_book, name='edit-book'),
    path('books/delete/<int:id>/', delete_book, name='delete-book'),
    path('books/qr/<int:id>/', generate_qr, name='book-qr'),

    # =========================
    # MEMBERS
    # =========================
    path('members/', member_list, name='members-page'),
    path('members/add/', add_member, name='add-member'),
    path('members/edit/<int:id>/', edit_member, name='edit-member'),
    path('members/delete/<int:id>/', delete_member, name='delete-member'),

    # =========================
    # ISSUE BOOKS
    # =========================
    path('issue/', issue_book_list, name='issue-books-page'),
    path('issue/add/', issue_book, name='issue-book'),

    # =========================
    # RETURN BOOK
    # =========================
    path('issue/return/<int:id>/', return_book, name='return-book'),
]