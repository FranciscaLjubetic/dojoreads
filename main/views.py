from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Books, Reviews, Author
from django.db.models import Count
from django.db.utils import IntegrityError



@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


@login_required
def books(request):
    usuarios = User.objects.all()
    libros = Books.objects.all()
    resenas = Reviews.objects.all()
    last_three = Reviews.objects.all().order_by('-created_at')[:3]
    autores = Author.objects.all()

    
    context ={
        'User': usuarios,
        'Books': libros,
        'Reviews': resenas,
        'newest_three_reviews': last_three,
        'Authors':autores,
        
    }
    return render(request, 'books.html', context)

@login_required
def booksadd(request):
    if request.method == 'GET':
        resenas = Reviews.objects.all()
        libros = Books.objects.all()
        autores = Author.objects.all()
        #estrellas =[]

        context = {
            'books' : libros,
            'Authors': autores,
            'Reviews': resenas,
            #'Estrellas': estrellas,
            
        }
        return render(request,"booksadd.html", context)

    
    else:
        errors = Books.objects.basic_validator(request.POST)
        autornuevo = None
        if request.POST['author_id'] == 'other':
            # en este caso hay que crearla
            new_author_name = request.POST['newAuthor']
            old_authors = Author.objects.filter(name__iexact=new_author_name)
            
            if len(old_authors) > 0:
                messages.error(request,"This author already exists.")
                return redirect("/books/add")
            autornuevo = Author.objects.create(name = new_author_name)
        
        else:  
            # en este caso hay que rescatarla de la DB
            author_id = int(request.POST['author_id'])
            autornuevo = Author.objects.get(id=author_id)
        
        # Ahora estamos 100% seguros que SI existe 'autornuevo'
        user_id = request.session['user']['id']
        usuario = User.objects.get(id= user_id)
        titulo = request.POST['title']
        resena = request.POST['review']
        score = int(request.POST['stars'])
        
        '''
        if score == 1:
            estrellas.add('★☆☆☆☆')
        elif rating == 2:
            estrellas.add('★★☆☆☆')
        elif rating == 3:
            estrellas.add('★★★☆☆')
        elif rating == 4:
            estrellas.add('★★★★☆')
        else:
            estrellas.add('★★★★★')
        '''
                
        if len(errors)> 0: #si el suscriptor lleno mal esta cuestion
            for key, error_message in errors.items():
                messages.error(request, error_message)
            return redirect(f'/books/add')
        
        old_books = Books.objects.filter(title__iexact=titulo)
        if len(old_books) > 0:
            messages.error(request,"This title already exists.")
            
        
        try:
            new_book = Books.objects.create(title = titulo, author= autornuevo)
            new_review = Reviews.objects.create(desc= resena, rating= score, user= usuario, book = new_book)
        except IntegrityError:
            messages.error(request,"This title already exists. You could write another review.")
            return redirect(f'/books/add')
            
        messages.success(request, 'Book successfully added and Author successfully linked to the book')
    return redirect('/books')
    

@login_required
def booksview(request, nom):
    if request.method =='GET':
        usuarios = User.objects.all()
        libros = Books.objects.all()
        resenas = Reviews.objects.all()
        autores = Author.objects.all()
        this_book = Books.objects.get(id = int(nom))
        this_book_reviews = this_book.review.all()
        
        bookids = []
        tot = 0
        for rev in this_book_reviews:
            bookids.append(rev.user_id)
            tot= rev.rating
        
        if len(bookids) == 0:
            tot_sum = 'No reviews yet'
        else:
            tot_sum = tot/len(bookids)
    
        #this_review_users = User.objects.filter(review__book= this_book)
        #this_forbidden_to_review_users = User.objects.get(review__book__User__id= you)
        context ={
            'User': usuarios,
            'Books': libros,
            'Reviews': resenas,
            'Author': autores,
            'this_book': this_book,
            'this_book_reviews': this_book_reviews,
            'bookids':bookids,
            'tot_sum': tot_sum,
            
            
        }
        return render(request, 'booksview.html', context)
    else:
        #lo que tengo que preguntar ahora es que si existen reseñas de este libro que sean de un user con el mismo id del sesion, entonces no puede agregar
        #una reseña nueva para ese libro. entonces if [user_id for user_id in this_book_reviews.user.id not in request.session.user.id]
        curr_user = request.session['user']
        fresh_resena = request.POST['new_review']
        nuevo_score = int(request.POST['new_stars'])
        new_resena = Reviews.objects.create(desc= fresh_resena, rating= nuevo_score, user= curr_user, book = this_book)
        messages.success(request, 'Review successfully linked to the book')
        return redirect(f'/books/{nom}')
        
        

@login_required
def userview(request, nem):
    usuarios = User.objects.all()
    libros = Books.objects.all()
    resenas = Reviews.objects.all()
    autores = Author.objects.all()
    this_user = User.objects.get(id= int(nem))
    this_user_revs = Reviews.objects.filter(user = this_user)
    this_user_total_reviews = []
    for rev in this_user_revs:
        this_user_total_reviews.append(rev)
    

    context ={
        'User': usuarios,
        'Books': libros,
        'Reviews': resenas,
        'Author': autores,
        'this_user': this_user,
        'this_user_total_reviews': len(this_user_total_reviews)
    }
    
    return render(request, 'userview.html', context)
    
        

@login_required
def deletereview(request, nim):
    this_review = Reviews.objects.get(id = int(nim))
    this_book_id = this_review.book.id
    this_user= this_review.user
    context ={
        'this_user': this_user
    }
    del this_review
    return redirect(f'/books/{this_book_id}')

def addreview(request, nam):
    this_book = Books.objects.get(id = int(nam))
    user_id = request.session['user']['id']
    usuario = User.objects.get(id= user_id)
    fresh_resena = request.POST['new_review']
    nuevo_score = int(request.POST['new_stars'])
    new_resena = Reviews.objects.create(desc= fresh_resena, rating= nuevo_score, user= usuario, book = this_book)
    messages.success(request, 'Review successfully linked to the book')
    return redirect(f'/books/{nam}')


#connected_user_id = request.session['user']['id']
#user_connected = request.session['user']
#got:reviewsonthisbookuser = User.filter.get(this_book__review__user__id= user_id)
#tengo



