"""
Test suite for main.py - Happy path scenarios
Tests database operations including User, Post, and Comment creation and retrieval.
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import Base, Comment, Post, User


class TestDatabaseOperationsHappyPath(unittest.TestCase):
    """Test happy path scenarios for database operations"""

    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests"""
        # Create a temporary database for testing
        cls.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_db_path = cls.temp_db.name
        cls.temp_db.close()

        cls.engine = create_engine(f"sqlite:///{cls.temp_db_path}", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Clean up test database after all tests"""
        cls.engine.dispose()
        if os.path.exists(cls.temp_db_path):
            os.unlink(cls.temp_db_path)

    def setUp(self):
        """Set up a fresh session for each test"""
        self.session = self.Session()

    def tearDown(self):
        """Clean up after each test"""
        self.session.rollback()
        self.session.close()
        # Clear all tables
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_create_tables(self):
        """Test that all required tables are created successfully"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        self.assertIn("user_account", tables)
        self.assertIn("post", tables)
        self.assertIn("comment", tables)

    def test_create_user_happy_path(self):
        """Test successful user creation with all required fields"""
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Verify user was created
        retrieved_user = self.session.query(User).filter_by(username="testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.fullname, "Test User")
        self.assertEqual(retrieved_user.email, "test@example.com")
        self.assertEqual(retrieved_user.password, "password123")
        self.assertIsNotNone(retrieved_user.created_at)
        self.assertIsNotNone(retrieved_user.updated_at)
        self.assertIsNone(retrieved_user.deleted_at)

    def test_create_post_happy_path(self):
        """Test successful post creation with all required fields"""
        # Create a user first
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Create a post
        post = Post(title="Test Post", content="This is a test post content", user_id=user.id)
        self.session.add(post)
        self.session.commit()

        # Verify post was created
        retrieved_post = self.session.query(Post).filter_by(title="Test Post").first()
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post.title, "Test Post")
        self.assertEqual(retrieved_post.content, "This is a test post content")
        self.assertEqual(retrieved_post.user_id, user.id)
        self.assertIsNotNone(retrieved_post.created_at)
        self.assertIsNotNone(retrieved_post.updated_at)
        self.assertIsNone(retrieved_post.deleted_at)

    def test_create_comment_happy_path(self):
        """Test successful comment creation with all required fields"""
        # Create a user first
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Create a post
        post = Post(title="Test Post", content="This is a test post content", user_id=user.id)
        self.session.add(post)
        self.session.commit()

        # Create a comment
        comment = Comment(content="This is a test comment", user_id=user.id, post_id=post.id)
        self.session.add(comment)
        self.session.commit()

        # Verify comment was created
        retrieved_comment = self.session.query(Comment).filter_by(content="This is a test comment").first()
        self.assertIsNotNone(retrieved_comment)
        self.assertEqual(retrieved_comment.content, "This is a test comment")
        self.assertEqual(retrieved_comment.user_id, user.id)
        self.assertEqual(retrieved_comment.post_id, post.id)
        self.assertIsNotNone(retrieved_comment.created_at)
        self.assertIsNotNone(retrieved_comment.updated_at)
        self.assertIsNone(retrieved_comment.deleted_at)

    def test_user_post_relationship_happy_path(self):
        """Test that user-post relationships work correctly"""
        # Create a user
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Create multiple posts for the user
        post1 = Post(title="Post 1", content="Content 1", user_id=user.id)
        post2 = Post(title="Post 2", content="Content 2", user_id=user.id)
        self.session.add_all([post1, post2])
        self.session.commit()

        # Verify relationships
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        self.assertEqual(len(retrieved_user.posts), 2)
        self.assertIn("Post 1", [p.title for p in retrieved_user.posts])
        self.assertIn("Post 2", [p.title for p in retrieved_user.posts])

        # Verify back reference
        retrieved_post = self.session.query(Post).filter_by(title="Post 1").first()
        self.assertEqual(retrieved_post.user.username, "testuser")

    def test_post_comment_relationship_happy_path(self):
        """Test that post-comment relationships work correctly"""
        # Create a user
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Create a post
        post = Post(title="Test Post", content="Test Content", user_id=user.id)
        self.session.add(post)
        self.session.commit()

        # Create multiple comments for the post
        comment1 = Comment(content="Comment 1", user_id=user.id, post_id=post.id)
        comment2 = Comment(content="Comment 2", user_id=user.id, post_id=post.id)
        self.session.add_all([comment1, comment2])
        self.session.commit()

        # Verify relationships
        retrieved_post = self.session.query(Post).filter_by(id=post.id).first()
        self.assertEqual(len(retrieved_post.comments), 2)
        self.assertIn("Comment 1", [c.content for c in retrieved_post.comments])
        self.assertIn("Comment 2", [c.content for c in retrieved_post.comments])

        # Verify back reference
        retrieved_comment = self.session.query(Comment).filter_by(content="Comment 1").first()
        self.assertEqual(retrieved_comment.post.title, "Test Post")

    def test_user_comment_relationship_happy_path(self):
        """Test that user-comment relationships work correctly"""
        # Create a user
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Create a post
        post = Post(title="Test Post", content="Test Content", user_id=user.id)
        self.session.add(post)
        self.session.commit()

        # Create multiple comments by the user
        comment1 = Comment(content="Comment 1", user_id=user.id, post_id=post.id)
        comment2 = Comment(content="Comment 2", user_id=user.id, post_id=post.id)
        self.session.add_all([comment1, comment2])
        self.session.commit()

        # Verify relationships
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        self.assertEqual(len(retrieved_user.comments), 2)
        self.assertIn("Comment 1", [c.content for c in retrieved_user.comments])
        self.assertIn("Comment 2", [c.content for c in retrieved_user.comments])

        # Verify back reference
        retrieved_comment = self.session.query(Comment).filter_by(content="Comment 1").first()
        self.assertEqual(retrieved_comment.user.username, "testuser")

    def test_timestamp_mixin_happy_path(self):
        """Test that timestamps are automatically set on creation"""
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Verify timestamps exist and are valid
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_soft_delete_happy_path(self):
        """Test that soft delete sets deleted_at timestamp"""
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Initially, deleted_at should be None
        self.assertIsNone(user.deleted_at)

        # Soft delete the user
        user.soft_delete()
        self.session.commit()

        # Verify deleted_at is now set
        self.assertIsNotNone(user.deleted_at)

    def test_restore_after_soft_delete_happy_path(self):
        """Test that restore clears deleted_at timestamp"""
        user = User(username="testuser", fullname="Test User", email="test@example.com", password="password123")
        self.session.add(user)
        self.session.commit()

        # Soft delete the user
        user.soft_delete()
        self.session.commit()
        self.assertIsNotNone(user.deleted_at)

        # Restore the user
        user.restore()
        self.session.commit()

        # Verify deleted_at is None again
        self.assertIsNone(user.deleted_at)

    def test_main_scenario_happy_path(self):
        """Test the exact scenario from main.py"""
        # Create user, post, and comment as in main.py
        user = User(username="test", fullname="Test User", email="test@example.com", password="password")
        self.session.add(user)
        self.session.commit()

        post = Post(title="Test Post", content="This is a test post", user_id=user.id)
        self.session.add(post)
        self.session.commit()

        comment = Comment(content="This is a test comment", user_id=user.id, post_id=post.id)
        self.session.add(comment)
        self.session.commit()

        # Verify all entities were created successfully
        self.assertEqual(self.session.query(User).count(), 1)
        self.assertEqual(self.session.query(Post).count(), 1)
        self.assertEqual(self.session.query(Comment).count(), 1)

        # Verify data integrity
        created_user = self.session.query(User).first()
        created_post = self.session.query(Post).first()
        created_comment = self.session.query(Comment).first()

        self.assertEqual(created_user.username, "test")
        self.assertEqual(created_post.title, "Test Post")
        self.assertEqual(created_comment.content, "This is a test comment")

        # Verify relationships
        self.assertEqual(created_post.user.id, created_user.id)
        self.assertEqual(created_comment.user.id, created_user.id)
        self.assertEqual(created_comment.post.id, created_post.id)

    def test_multiple_users_posts_comments_happy_path(self):
        """Test creating multiple users, posts, and comments"""
        # Create multiple users
        user1 = User(username="user1", fullname="User One", email="user1@example.com", password="password1")
        user2 = User(username="user2", fullname="User Two", email="user2@example.com", password="password2")
        self.session.add_all([user1, user2])
        self.session.commit()

        # Create posts for each user
        post1 = Post(title="Post 1", content="Content 1", user_id=user1.id)
        post2 = Post(title="Post 2", content="Content 2", user_id=user2.id)
        self.session.add_all([post1, post2])
        self.session.commit()

        # Create comments
        comment1 = Comment(content="Comment 1", user_id=user1.id, post_id=post1.id)
        comment2 = Comment(content="Comment 2", user_id=user2.id, post_id=post2.id)
        comment3 = Comment(content="Comment 3", user_id=user1.id, post_id=post2.id)
        self.session.add_all([comment1, comment2, comment3])
        self.session.commit()

        # Verify counts
        self.assertEqual(self.session.query(User).count(), 2)
        self.assertEqual(self.session.query(Post).count(), 2)
        self.assertEqual(self.session.query(Comment).count(), 3)

        # Verify relationships
        self.assertEqual(len(user1.posts), 1)
        self.assertEqual(len(user2.posts), 1)
        self.assertEqual(len(user1.comments), 2)  # user1 commented on post1 and post2
        self.assertEqual(len(user2.comments), 1)
        self.assertEqual(len(post1.comments), 1)
        self.assertEqual(len(post2.comments), 2)  # post2 has 2 comments


if __name__ == "__main__":
    unittest.main()
