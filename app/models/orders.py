from app import db
from app.constants import status
from datetime import datetime
from pytz import timezone


class Orders(db.Model):
    """
    Define the new Order class with the following Columns & relationships

    order_number -- Column: String(64)
    suborder_no -- Column: BigInteger, PrimaryKey
    date_submitted -- Column: DateTime -- date order was submitted
    date_received -- Column: DateTime -- day we receive order
    billing_name -- Column: String(64)
    customer_email -- Column: String(64)
    confirmation_message -- Column: Text
    client_data -- Column: Text
    client_id -- Column: Integer
    client_agency_name -- Column: String(64)
    """

    __tablename__ = 'orders'
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    # suborder_no = db.Column(db.BigInteger, primary_key=True, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=True)
    # billing_name = db.Column(db.String(64), nullable=False)
    # customer_email = db.Column(db.String(64), nullable=False)
    confirmation_message = db.Column(db.Text, nullable=False)
    client_data = db.Column(db.Text, nullable=False)
    # client_id = db.Column(db.Integer, nullable=False)
    # client_agency_name = db.Column(db.String(64), nullable=False)
    ordertypes = db.Column(db.String(255), nullable=True)
    suborders = db.relationship('Suborders', backref='suborders', lazy=True)
    customer = db.relationship('Customer', backref=db.backref('customer', uselist=False))
    # uselist = false backref='orders' -- old way I had it

    def __init__(
            self,
            id,
            # suborder_no,
            date_submitted,
            date_received,
            # billing_name,
            # customer_email,
            confirmation_message,
            client_data,
            # client_id,
            # client_agency_name,
            ordertypes,

    ):
        self.id = id
        # self.suborder_no = suborder_no
        self.date_submitted = date_submitted
        self.date_received = date_received or None
        # self.billing_name = billing_name
        # self.customer_email = customer_email
        self.confirmation_message = confirmation_message
        self.client_data = client_data
        # self.client_id = client_id
        # self.client_agency_name = client_agency_name
        self.ordertypes = ordertypes

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'order_no': self.order_no,
            'suborder_no': self.suborder_no,
            'date_submitted': self.date_submitted,
            'date_received': self.date_received.strftime("%x %I:%M %p"),
            'billing_name': self.billing_name,
            'customer_email': self.customer_email,
            'confirmation_message': self.confirmation_message,
            'client_data': self.client_data,
            'client_id': self.client_id,
            'client_agency_name': self.client_agency_name,
            'current_status': self.status.filter_by(suborder_no=self.suborder_no)
                                         .order_by(StatusTracker.id.desc()).first().current_status
        }


class Suborders(db.Model):
    """

    """
    __tablename__ = 'suborders'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    client_agency_name = db.Column(db.String(64), nullable=False)
    order_no = db.Column(db.String(64), db.ForeignKey('orders.id'), nullable=False)
    status = db.relationship('StatusTracker', backref=db.backref('suborders'), lazy='dynamic')

    def __init__(
            self,
            id,
            client_id,
            client_agency_name,
            order_no
    ):
        self.id = id
        self.client_id = client_id
        self.client_agency_name = client_agency_name
        self.order_no = order_no


class StatusTracker(db.Model):

    """
    Need to make a model that will change the status of the
    process of the document

    id - db.Integer , primary key = true
    suborder_no - Column: BigInteger, Foreign Key - connects the sub_order# to the top of this database
    status - Column: Enum - Tracks the status of the order can only be these set things
    comment - Column: db.String(64) - stores the comment that was passed in
    timestamp - Column: db.datetime - holds the time that the status was updated
    previous_value - Column: db.String(25) - Stores the previous status

    1. Received || Set to this by default
    2. Processing
        a)found
        b)printed
    3. Mailed/Pickup
    4. Not_Found
        a)Letter_generated
        b)Undeliverable - Cant move down the line
    5. Done - End of status changes

    """
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborders.id'), nullable=False)
    current_status = db.Column(
        db.Enum(
            status.RECEIVED,
            status.PROCESSING,
            status.FOUND,
            status.MAILED_PICKUP,
            status.NOT_FOUND,
            status.LETTER_GENERATED,
            status.UNDELIVERABLE,
            status.DONE,
            name='current_status'), nullable=True)
    comment = db.Column(db.String(64), nullable=True)
    timestamp = db.Column(db.DateTime)
    previous_value = db.Column(db.String(25), nullable=True)

    # Class Constructor to initialize the data
    def __init__(
                self,
                suborder_no,
                current_status,
                comment,
                timestamp,
                previous_value,
    ):
        self.suborder_no = suborder_no
        self.current_status = current_status
        self.comment = comment or None
        self.timestamp = timestamp or datetime.utcnow()
        self.previous_value = previous_value or None

    @staticmethod
    def utc_to_local(date):
        """Offsets the UTC into EST Timezone """
        return date + timezone('America/New_York').localize(date).utcoffset()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'suborder_no': self.suborder_no,
            'current_status': self.current_status,
            'comment': self.comment,
            'timestamp': self.utc_to_local(self.timestamp).strftime("%x %I:%M %p"),
            'previous_value': self.previous_value,
        }
