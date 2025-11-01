from core.database import create_tables, get_session
from models.models import Comment, Post, User

if __name__ == "__main__":
    create_tables()
    Session = get_session()
    with Session() as session:
        session.add(User(username="test", fullname="Test User", email="test@example.com", password="password"))
        session.add(Post(title="Test Post", content="This is a test post", user_id=1))
        session.add(Comment(content="This is a test comment", user_id=1, post_id=1))
        session.commit()
        print("Tablas creadas correctamente")
