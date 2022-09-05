from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    # content = StringField('Content',validators=[DataRequired()],widget=TextArea())
    content = CKEditorField('Content',validators=[DataRequired()])
    slug = StringField('Slug',validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField('Searched',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(),Length(min=5, max=500)])
    submit = SubmitField('Add Comment')

