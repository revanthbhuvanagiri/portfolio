from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from typing import List, Optional
import logging
from werkzeug.utils import secure_filename
import markdown

app = Flask(__name__)
# Move configuration to config.py in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-for-development')

db = SQLAlchemy(app)

# Add this after creating the app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Project(db.Model):
    """Model for portfolio projects"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    technologies = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Project {self.title}>'

class Contact(db.Model):
    """Model for contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Contact {self.name}>'

class Blog(db.Model):
    """Model for blog posts"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    tags = db.Column(db.String(200))  # Comma-separated tags

    def __repr__(self) -> str:
        return f'<Blog {self.title}>'

    @property
    def html_content(self):
        """Convert markdown content to HTML"""
        return markdown.markdown(self.content)

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/projects')
def projects():
    """Projects page route"""
    try:
        projects: List[Project] = Project.query.order_by(Project.created_at.desc()).all()
        project_count = len(projects)
        logger.info(f"Found {project_count} projects in database")
        
        if not projects:
            logger.info("No projects found in database")
            return render_template('projects.html', projects=[], message="No projects available yet.")
            
        # Log the first project for debugging
        if project_count > 0:
            logger.info(f"Sample project: {projects[0].title}")
            
        return render_template('projects.html', projects=projects)
    except Exception as e:
        logger.error(f"Error loading projects: {str(e)}")
        flash('Unable to load projects. Please try again later.', 'error')
        return render_template('projects.html', projects=[], message="Error loading projects.")

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route with form handling"""
    if request.method == 'POST':
        try:
            new_message = Contact(
                name=request.form.get('name', ''),
                email=request.form.get('email', ''),
                message=request.form.get('message', '')
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Thank you for your message! I will get back to you soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of blogs per page
    
    try:
        blogs = Blog.query.filter_by(published=True)\
            .order_by(Blog.created_at.desc())\
            .paginate(page=page, per_page=per_page)
        return render_template('blog/index.html', blogs=blogs)
    except Exception as e:
        logger.error(f"Error loading blogs: {str(e)}")
        flash('Unable to load blog posts. Please try again later.', 'error')
        return render_template('blog/index.html', blogs=None)

@app.route('/blog/<slug>')
def blog_detail(slug):
    """Individual blog post page"""
    try:
        blog = Blog.query.filter_by(slug=slug, published=True).first_or_404()
        return render_template('blog/detail.html', blog=blog)
    except Exception as e:
        logger.error(f"Error loading blog post: {str(e)}")
        flash('Unable to load blog post. Please try again later.', 'error')
        return redirect(url_for('blog'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
