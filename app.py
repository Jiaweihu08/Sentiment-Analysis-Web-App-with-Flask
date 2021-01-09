from flask import Flask, render_template, flash, url_for
from forms import SentimentText
from sentiment import get_sentiment


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'


@app.route('/', methods=['GET', 'POST'])
def sentiment():
	form = SentimentText()
	if form.validate_on_submit():
		text, sentiment, file_name = get_sentiment(form.text.data)
		image_source = url_for('static',
			filename='results/'+file_name)
		flash(f"The sentiment of the text is {sentiment}", "success")
	else:
		text = None
		image_source = None
	return render_template('sentiment.html',
		title='Sentiment Analysis',
		form=form,
		text=text,
		image_source=image_source)


if __name__ == '__main__':
	app.run(debug=True)