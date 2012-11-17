from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///ele_project.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
									autocommit = False,
									autoflush = False))
Base = declarative_base()
Base.query = session.query_property()


#-------------------------------------------General functions:
def new_thing(db, table, columns, values):
	"""insert a new user, post, comment into the database"""
	pass
	# thing = 
	# session.add(thing)
	# session.commit()

def get_thing(db, id):
	"""retrieve a user, post, comment with its id"""
	pass

#--------------------------------------------CLASSES definition:
#-------------------User Class----------------------------------
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(80), nullable=False)
	password = Column(String(10), nullable=False)
	username = Column(String(20), nullable=True)

	#--------class attributes-----------------
    # COLS = ["id", "email", "password", "username"]
    # TABLE_NAME = "users"
	#--------class methods--------------------
	@classmethod
	def authenticate(cls, email, password):
		auth = session.query(User).filter_by(email=email, password=password).first()
		return auth

	@classmethod
	def new(cls, db, email, password, username):
		user = User()
		return new_thing()

	@classmethod
	def get(cls, db, id):
		pass
		return get_thing()

	#--------instance methods------------------
	def get_id(self, db, email, password, username):
		pass

	def get_posts(self, db, id):
		pass
	
#-------------------Post Class----------------------------------
class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key = True)
	sound = Column(String(150), nullable=False)
	text = Column(String(150), nullable=False)
	posted_at = Column(DateTime())
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship("User",
		backref=backref("posts", order_by=id))

	#--------class attributes-----------------
    # COLS = ["id", "sound", "text", "posted_at", "user_id"]
    # TABLE_NAME = "posts"
	#--------class methods--------------------
	@classmethod
	def new(cls, db, email, password, username):
		pass
		return new_thing()

	@classmethod
	def get(cls, db, id):
		pass
		return get_thing()

	#--------instance methods------------------
	def get_id(self, db, sound, text, posted_at, user_id):
		pass

#-------------------Comment Class----------------------------------
class Comment(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key = True)
	sound = Column(String(150), nullable=True)
	text = Column(String(150), nullable=False)
	posted_at = Column(DateTime())
	user_id = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))

	user = relationship("User",
		backref=backref("comments", order_by=id))

	post = relationship("Post",
		backref=backref("comments", order_by=id))

	#--------class attributes-----------------
    # COLS = ["id", "sound", "text", "posted_at", "user_id", "post_id"]
    # TABLE_NAME = "comments"
	#--------class methods--------------------
	@classmethod
	def new(cls, db, email, password, username):
		pass
		return new_thing()

	@classmethod
	def get(cls, db, id):
		pass
		return get_thing()

	#--------instance methods------------------
	def get_id(self, db, sound, text, posted_at, user_id, post_id):
		pass

#End of Classes definition



def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()