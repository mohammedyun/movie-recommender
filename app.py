from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model and data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return []
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    movie_name = ""
    if request.method == 'POST':
        movie_name = request.form.get('movie')
        recommendations = recommend(movie_name)
    return render_template('index.html', recommendations=recommendations, movie_name=movie_name)

if __name__ == '__main__':
    app.run(debug=True)
