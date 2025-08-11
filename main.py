from flask import Flask, render_template, request, redirect,url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

app = Flask(__name__)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase: Client = create_client(url, key)

@app.route('/', endpoint='home')
def index():
        # Fetch all projects
    response = supabase.table("projects").select("*").execute()
    return render_template('index.html', projects=response.data)

@app.route("/blog")
def blog():
    response = supabase.table("blogs").select("*").execute()
    return render_template('blog.html', posts=response.data)

# @app.route('/projects')
# def projects():
#     # Fetch all projects
#     response = supabase.table("projects").select("*").execute()
#     return render_template('index.html', projects=response.data)

# @app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':    
        title = request.form.get('title')
        description = request.form.get('description')
        github_url = request.form.get('github_url')

        if not title or not description:
            return "Title and Description are required!", 400

        supabase.table("projects").insert({
            "title": title,
            "description": description,
            "github_url": github_url
        }).execute()

        return redirect('/projects')  # Change as needed

    return render_template('add_project.html')


if __name__ == '__main__':
    app.run(debug=True)
