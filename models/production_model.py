from database import db
import uuid
class Production(db.Model):
    __tablename__ = 'productions'
    id = db.Column(db.String, name="uuid", primary_key=True, default=uuid.uuid4())
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)