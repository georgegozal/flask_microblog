from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
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