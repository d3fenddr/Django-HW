from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from app.models import Category


def main():
    url = os.getenv('HABR_API_DATABASE_URL', 'sqlite:///./habr_api.db')
    engine = create_engine(url)
    with Session(engine) as db:
        predefined = [
            ('Backend', 'backend'),
            ('Frontend', 'frontend'),
            ('AI', 'ai'),
            ('Cyber Security', 'cyber-security'),
            ('Cyber Sport', 'cyber-sport'),
            ('Game Development', 'game-dev'),
        ]
        for name, slug in predefined:
            exists = db.query(Category).filter(Category.slug == slug).first()
            if not exists:
                db.add(Category(name=name, slug=slug))
        db.commit()
    print('Categories seeded.')


if __name__ == '__main__':
    main()


