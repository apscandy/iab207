from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db

bp = Blueprint('destination', __name__, url_prefix='/destinations')

@bp.route('/<id>')
def show(id):
    destination = Destination.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=cform)

@bp.route('/create', methods = ['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    destination = Destination(name=form.name.data,
    description= form.description.data,
    image=form.image.data,
    currency=form.currency.data)
    # add the object to the db session
    db.session.add(destination)
    # commit to the database
    db.session.commit()
    print('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

@bp.route('/<destination>/comment', methods = ['GET', 'POST'])  
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Destination.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=destination))
    