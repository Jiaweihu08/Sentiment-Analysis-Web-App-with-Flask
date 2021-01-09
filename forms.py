from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SentimentText(FlaskForm):
	text = TextAreaField('Enter your text below to analyze.',
		validators=[DataRequired(), Length(min=5, max=500)])
	submit = SubmitField('Analyze Sentiment')