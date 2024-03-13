# These routes are an example of how to use data, forms and routes to create
# a forum where a blogs and comments on those blogs can be
# Created, Read, Updated or Deleted (CRUD)

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Animal, Comment
from app.classes.forms import AnimalForm, CommentForm
from flask_login import login_required
import datetime as dt

@app.route('/animal/list')
@app.route('/animals')
@login_required
def animalList():
    animals = Animal.objects()
    return render_template('animals.html',animals=animals)


@app.route('/animal/<animalID>')
@login_required
def animal(animalID):
    thisAnimal = Animal.objects.get(id=animalID)
    return render_template('animal.html',animal=thisAnimal)


@app.route('/animal/delete/<animalID>')
@login_required
def animalDelete(animalID):
    deleteAnimal = Animal.objects.get(id=animalID)
    if current_user == deleteAnimal.author:
        deleteAnimal.delete()
        flash('The Animal was deleted.')
    else:
        flash("You can't delete a animal you don't own.")
    animals = Animal.objects()  
    return render_template('animals.html',animals=animals)

@app.route('/animal/new', methods=['GET', 'POST'])
@login_required
def animalNew():
    form = AnimalForm()

    if form.validate_on_submit():
        newAnimal = Animal(
            animaltype = form.animaltype.data,
            animalname = form.animalname.data,
            animalgender = form.animalgender.data,
            animalage = form.animalage.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        newAnimal.save()

        return redirect(url_for('animal',animalID=newAnimal.id))
    return render_template('animalform.html',form=form)


@app.route('/animal/edit/<animalID>', methods=['GET', 'POST'])
@login_required
def animalEdit(animalID):
    editAnimal = Animal.objects.get(id=animalID)
    if current_user != editAnimal.author:
        flash("You can't edit a animal you don't own.")
        return redirect(url_for('animal',animalID=animalID))
    # get the form object
    form = AnimalForm()
    if form.validate_on_submit():
        editAnimal.update(
            animaltype = form.animaltype.data,
            animalname = form.animalname.data,
            animalgender = form.animalgender.data,
            animalage = form.animalage.data,
            modify_date = dt.datetime.utcnow
        )
        return redirect(url_for('animal',animalID=animalID))

    form.animaltype.data = editAnimal.animaltype
    form.animalname.data = editAnimal.animalname
    form.animalgender.data = editAnimal.animalgender
    form.animalage.data = editAnimal.animalage

    return render_template('animalform.html',form=form)


# @app.route('/comment/new/<animalID>', methods=['GET', 'POST'])
# @login_required
# def commentNew(animalID):
#     animal = Animal.objects.get(id=animalID)
#     form = CommentForm()
#     if form.validate_on_submit():
#         newComment = Comment(
#             author = current_user.id,
#             animal = animalID,
#             content = form.content.data
#         )
#         newComment.save()
#         return redirect(url_for('animal',animalID=animalID))
#     return render_template('commentform.html',form=form,animal=animal)

# @app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
# @login_required
# def commentEdit(commentID):
#     editComment = Comment.objects.get(id=commentID)
#     if current_user != editComment.author:
#         flash("You can't edit a comment you didn't write.")
#         return redirect(url_for('animal',animalID=editComment.animal.id))
#     animal = Animal.objects.get(id=editComment.animal.id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         editComment.update(
#             content = form.content.data,
#             modifydate = dt.datetime.utcnow
#         )
#         return redirect(url_for('animal',animalID=editComment.animal.id))

#     form.content.data = editComment.content

#     return render_template('commentform.html',form=form,animal=animal)   

# @app.route('/comment/delete/<commentID>')
# @login_required
# def commentDelete(commentID): 
#     deleteComment = Comment.objects.get(id=commentID)
#     deleteComment.delete()
#     flash('The comments was deleted.')
#     return redirect(url_for('animal',animalID=deleteComment.animal.id)) 
