from app import app, db, Project, Blog
import logging
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Seed the database with sample projects"""
    try:
        with app.app_context():
            # Drop all tables and create them again
            db.drop_all()
            db.create_all()
            logger.info("Database tables recreated successfully")
            
            # Create sample projects
            projects = [
                Project(
                    title="AI Chatbot",
                    description="A conversational AI chatbot built using transformers and GPT models",
                    image_url="https://placehold.co/600x400",
                    github_url="https://github.com/yourusername/chatbot",
                    live_url="https://chatbot-demo.com",
                    technologies="Python, Transformers, Flask, JavaScript",
                    created_at=datetime.utcnow()
                ),
                Project(
                    title="Image Recognition App",
                    description="Deep learning-based image recognition application using CNN",
                    image_url="https://placehold.co/600x400",
                    github_url="https://github.com/yourusername/image-recognition",
                    live_url="https://image-recognition-demo.com",
                    technologies="Python, TensorFlow, OpenCV, Flask",
                    created_at=datetime.utcnow()
                ),
                Project(
                    title="Gen AI Assistant",
                    description="An AI-powered assistant for code generation and analysis",
                    image_url="https://placehold.co/600x400",
                    github_url="https://github.com/yourusername/gen-ai",
                    live_url="https://gen-ai-demo.com",
                    technologies="Python, LangChain, OpenAI, React",
                    created_at=datetime.utcnow()
                )
            ]
            
            # Add projects to database
            for project in projects:
                db.session.add(project)
            
            db.session.commit()
            logger.info("Sample projects added successfully!")
            
            # Verify projects were added
            project_count = Project.query.count()
            logger.info(f"Number of projects in database: {project_count}")
            
            # Create sample blog posts
            blogs = [
                Blog(
                    title="Getting Started with AI Development",
                    slug="getting-started-with-ai",
                    content="""
# Getting Started with AI Development

Artificial Intelligence is revolutionizing the way we build software. In this post, we'll explore the basics of AI development.

## Key Topics

1. Understanding Machine Learning
2. Popular AI Frameworks
3. Best Practices

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    """,
                    summary="A beginner's guide to AI development and machine learning fundamentals",
                    image_url="https://placehold.co/800x400",
                    tags="AI, Machine Learning, Programming",
                    created_at=datetime.utcnow() - timedelta(days=5)
                ),
                Blog(
                    title="Building Neural Networks with PyTorch",
                    slug="neural-networks-pytorch",
                    content="""
# Building Neural Networks with PyTorch

PyTorch is a powerful framework for deep learning. Let's explore how to build neural networks.

## Topics Covered

1. PyTorch Basics
2. Neural Network Architecture
3. Training Models

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    """,
                    summary="Learn how to create and train neural networks using PyTorch",
                    image_url="https://placehold.co/800x400",
                    tags="PyTorch, Deep Learning, Neural Networks",
                    created_at=datetime.utcnow() - timedelta(days=2)
                )
            ]
            
            # Add blogs to database
            for blog in blogs:
                db.session.add(blog)
            
            db.session.commit()
            logger.info("Sample blog posts added successfully!")
            
            # Verify blog posts were added
            blog_count = Blog.query.count()
            logger.info(f"Number of blog posts in database: {blog_count}")
            
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.session.rollback()
        raise e

if __name__ == "__main__":
    seed_database() 