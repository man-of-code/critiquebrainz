from critiquebrainz.data import db
from sqlalchemy.dialects.postgresql import UUID
from critiquebrainz.utils import generate_string


class OAuthClient(db.Model):
    __tablename__ = 'oauth_client'

    client_id = db.Column(db.Unicode, primary_key=True)
    client_secret = db.Column(db.Unicode, nullable=False)
    redirect_uri = db.Column(db.UnicodeText, nullable=False)

    user_id = db.Column(UUID, db.ForeignKey('user.id', ondelete='CASCADE'))
    name = db.Column(db.Unicode, nullable=False)
    desc = db.Column(db.Unicode, nullable=False)
    website = db.Column(db.Unicode, nullable=False)

    grants = db.relationship('OAuthGrant', cascade='all', backref='client')
    tokens = db.relationship('OAuthToken', cascade='all', backref='client')

    allowed_includes = []

    @classmethod
    def generate(cls, user, name, desc, website, redirect_uri):
        client_id = generate_string(20)
        client_secret = generate_string(40)
        client = cls(client_id=client_id, client_secret=client_secret,
                     user=user, name=name, desc=desc, website=website, redirect_uri=redirect_uri)
        db.session.add(client)
        db.session.commit()
        return client

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        response = dict(client_id=self.client_id,
                        client_secret=self.client_secret,
                        user_id=self.user_id,
                        name=self.name,
                        desc=self.desc,
                        website=self.website,
                        redirect_uri=self.redirect_uri)
        return response

    def update(self, name=None, desc=None, website=None, redirect_uri=None):
        if name is not None:
            self.name = name
        if desc is not None:
            self.desc = desc
        if website is not None:
            self.website = website
        if redirect_uri is not None:
            self.redirect_uri = redirect_uri
        db.session.commit()
