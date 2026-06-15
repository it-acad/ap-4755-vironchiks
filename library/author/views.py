from django.shortcuts import render, redirect
from .models import Author

def author_list(request):
    authors = Author.get_all() 
    return render(request, 'author/author_list.html', {'authors': authors})

def create_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')

        if name and surname and patronymic:
            Author.create(name=name, surname=surname, patronymic=patronymic)
            return redirect('author_list')
        
    return render(request, 'author/create_author.html')

def delete_author(request, author_id):
    if request.method == 'POST':
        author = Author.get_by_id(author_id)
        if author:
            # Перевіряємо, чи немає в автора книг
            if not hasattr(author, 'book_set') or not author.book_set.exists():
                Author.delete_by_id(author_id)
            else:
                print("У цього автора є книги, видаляти не можна!")
                
    return redirect('author_list')