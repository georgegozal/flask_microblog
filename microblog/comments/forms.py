from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length
# from flask_ckeditor import CKEditorField

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(),Length(min=5, max=500)])
    submit = SubmitField('Add Comment')

