from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///ele_wordsana.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
									autocommit = False,
									autoflush = False))
Base = declarative_base()
Base.query = session.query_property()


#-------------------------------------------General functions:
def new_thing(table, columns, values):
	"""insert a new user, post, comment into the database"""
	pass
	#insert in a specific table the values given taking into account the 
	#columns order
	
	# thing = table(values)
	# session.add(thing)
	# session.commit()

def get_thing(id):
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

	def __init__(self, email, password, username):
		self.email = email
		self.password = password
		self.username = username

	#--------class methods--------------------
	@classmethod
	def authenticate(cls, email, password):
		auth = session.query(User).filter_by(email=email, password=password).first()
		return auth

	@classmethod
	def new(cls, email, password, username):
		user = User(email, password, username)
		session.add(user)
		session.commit()
		return user

	@classmethod
	def get(cls, id):
		user = session.query(User).get(id)
		return user

	@classmethod
	def check_name(cls, username):
		"""checks if a username is already used by another user."""
		check = session.query(User).filter_by(username=username).first()
		return check

	#--------instance methods------------------
	# def get_id(self, email, password, username):
	# 	"""retrieves the id of a particular user"""
	# 	user_id = session.query(User).filter_by(email=email, password=password, username=username)
	# 	return user_id

	def get_posts(self, user_id):
		row_collection = session.query(Post).filter_by(user_id=user_id).order_by(Post.id.desc()).all()
		return row_collection

	def get_post(self, user_id):
		"""get Post using its id """
		post = session.query(Post).get(id)
		return post
	# def get_posts_ids(self, user_id):
	# 	row_collection = session.query(Post).filter_by(user_id=user_id).all()
	# 	sound_collection = []
	# 	for row in row_collection:
	# 		sound_id = row.id
	# 		sound_collection.append(sound_id)
	# 	return sound_collection

	# def get_posts_texts(self, user_id):
	# 	row_collection = session.query(Post).filter_by(user_id=user_id).all()
	# 	sound_collection = []
	# 	for row in row_collection:
	# 		sound_id = row.text
	# 		sound_collection.append(sound_id)
	# 	return sound_collection

	def change_password(self, id, new_password):
		user = session.query(User).get(id)
		user.password = new_password
		session.commit()
	
#-------------------Post Class----------------------------------
class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key = True)
	sound = Column(String(150), nullable=True)
	text = Column(String(150), nullable=True)
	posted_at = Column(DateTime())
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship("User",
		backref=backref("posts", order_by=id))

	def __init__(self, sound, text, posted_at, user_id):
		self.sound = sound
		self.text = text
		self.posted_at = posted_at
		self.user_id = user_id

	#--------class methods--------------------
	@classmethod
	def new(cls, sound, text, posted_at, user_id):
		now = datetime.datetime.now()
		post = Post(None, text, now, user_id)
		session.add(post)
		session.commit()
		return post

	@classmethod
	def get(cls, id):
		"""get Post using its id """
		post = session.query(Post).get(id)
		return post

	@classmethod
	def all(cls):
		posts = session.query(Post).all()
		return posts

	#--------instance methods------------------
	def get_id(self, sound, text, posted_at, user_id):
		pass

	def add_sound(self, post_id, sound_url):
		post = session.query(Post).get(post_id)
		post.sound = sound_url
		session.commit()

	# def get_comments(self, post_id, user_id):
	# 	comments = session.query(Comment).filter_by(post_id=post_id, user_id=user_id).all()
	# 	return comments

	def get_comments(self, post_id):
		comments = session.query(Comment).filter_by(post_id=post_id).all()
		return comments

	def num_likes(self, post_id):
		pass
		# likes = session.query(Comment).filter_by(post_id=post_id, text==None).all()
		# # all_comments = session.query(func.count(Comment.id))
		# # comments = session.query(func.count(Comment.text))
		# # likes = all_comments - comments
		# return likes

	def num_comments(self, post_id):
		pass
		# comments = session.query(Comment).filter_by(post_id=post_id, text!=None).all()
		# # comments = session.query(func.count(Comment.text))
		# return comments

#-------------------Comment Class----------------------------------
class Comment(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key = True)
	like = Column(Boolean, default=False)
	sound = Column(String(150), nullable=True)
	text = Column(String(150), nullable=True)
	posted_at = Column(DateTime())
	user_id = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))

	user = relationship("User",
		backref=backref("comments", order_by=id))

	post = relationship("Post",
		backref=backref("comments", order_by=id))

	def __init__(self, like, sound, text, posted_at, user_id, post_id):
		self.sound = sound
		selflike = like
		self.text = text
		self.posted_at = posted_at
		self.user_id = user_id
		self.post_id = post_id

	#--------class methods--------------------
	@classmethod
	def new_like(cls, like, sound, text, posted_at, user_id, post_id):
		""" a "like" is a comment without sound or text """
		now = datetime.datetime.now()
		like = Comment(1, None, None, now, user_id, post_id)
		session.add(like)
		session.commit()
		return like
		
	@classmethod
	def check_like(cls, like, user_id, post_id):
		prev_like = session.query(Comment).filter_by(like=1, user_id=user_id, post_id=post_id).first()
		return prev_like

	@classmethod
	def new_comment(cls, like, sound, text, posted_at, user_id, post_id):
		""" a "comment" has text and can have sound """
		now = datetime.datetime.now()
		comment = Comment(0, None, text, now, user_id, post_id)
		session.add(comment)
		session.commit()
		return comment

	@classmethod
	def get(cls, id):
		pass
		return get_thing()

	#--------instance methods------------------
	def get_id(self, sound, text, posted_at, user_id, post_id):
		pass

	# def get_comments(self, post_id, user_id):
	# 	comments = session.query(Comment).filter_by(post_id=post_id, user_id=user_id).all()
	# 	return comments


#End of Classes definition



def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()