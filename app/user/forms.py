from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class ProfileForm(FlaskForm):
    username = StringField('username', validators=[Length(0, 7)])
    about_me = PageDownField('about me', validators=[Length(0, 140)])

class PostForm(FlaskForm):
    body = TextAreaField('Blog', validators=[DataRequired()])
    title = StringField('Title', validators=[Length(1, 20)])
    # outline = StringField('Outline', validators=[Length()])
    save_draft = SubmitField('Save as draft')
    submit = SubmitField('Post')

class EditpostForm(FlaskForm):
    title = StringField('Title', validators=[Length(1, 20)])
    body = TextAreaField('Edit blog', validators=[DataRequired()])
    update = SubmitField('Update')
    submit = SubmitField('Post')
    save_draft = SubmitField('Save')

class CommentForm(FlaskForm):
    body = PageDownField('Comment', validators=[DataRequired()])

class ReplyForm(FlaskForm):
    body = PageDownField('Reply', validators=[DataRequired()])

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
