from flask import Flask, render_template, request
import viz as viz

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    '''
    Index page
    '''
    return render_template('index.html')

@app.route('/sentiment')
def sentiment():
    '''
    Page displaying sentiment of tweets
    '''
    line = viz.sent_line_plot()
    return render_template('sentiment.html', plot=line)

@app.route('/tweet_numbers')
def tweet_numbers():
    '''
    Page displaying number of tweets gathered to date
    '''
    bar = viz.number_tweets_barplot()
    return render_template('tweet_numbers.html', plot=bar)

@app.route('/sentiment_map')
def sentiment_map():
    '''
    Page displaying state-by-state map of sentiment across the US
    '''
    input = dict(request.args)
    ticket=input['ticket']
    map = viz.sentiment_map(ticket)
    return render_template('sentiment_map.html', plot=map, ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)
