from datetime import date, timedelta, datetime, time
from flask import jsonify, abort, request
from sqlalchemy import desc
from app.models import Order, Suborder, StatusTracker
from app.api_1_0 import api_1_0 as api
from app.api_1_0.utils import (
    update_status,
    get_orders_by_fields,
    login_user,
    _print_orders,
    _print_large_labels,
    _print_small_labels
)


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['GET', 'POST'])
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with today's date.

    As a user, I want to be able to search for specific orders.

    GET {order_no, suborder_no, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in utils.py

    :return {orders, 200}

        "billingname": "Jeffrey Kobacker",
        "clientagencyname": "Death Search",
        "clientdata": "ClientID|10000103|ClientAgencyName|Department of Record|OrderNo|9127848504|LASTNAME|Bloch|FIRSTNAME|Isaac|MIDDLENAME|S|RELATIONSHIP|Great Grandson|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|7|DEATH_PLACE|Manhattan, New York|AGEOFDEATH|78|YEAR_|1918,|BOROUGH|MANHATTAN,|",
        "clientid": 10000103,
        "confirmationmessage": "\nLast name:               Bloch\nFirst name:              Isaac\nMiddle name:             S\n\nMonth:                   December\nDay:                     7\nYear:                    1918\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          Manhattan, New York\nAge at Death:            78\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Great Grandson\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\n--------------------------------------------------------------------------------\n\n",
        "customeremail": "jkobacker@gmail.com",
        "datereceived": "2017-04-04 04:06:15",
        "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
        "orderno": "000592000",
        "suborderno": 9127848504

    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        order_no = json.get("order_no")
        suborder_no = json.get("suborder_no")
        order_type = json.get("order_type")
        billing_name = json.get("billing_name")
        user = ''
        date_submitted_start = json.get("date_submitted_start")
        date_submitted_end = json.get("date_submitted_end")

        order_count, suborder_count, orders = get_orders_by_fields(order_no,
                                                                   suborder_no,
                                                                   order_type,
                                                                   billing_name,
                                                                   user,
                                                                   date_submitted_start,
                                                                   date_submitted_end)
        return jsonify(all_orders=orders)

    else:
        yesterday = date.today() - timedelta(1)
        # Add time to date object
        yesterday_dt = datetime.combine(yesterday, time.min)

        orders = []
        for order in Order.query.filter(Order.date_submitted >= yesterday_dt):
            for suborder in order.suborder:
                orders.append(suborder.serialize)
        return jsonify(all_orders=orders)


@api.route('/status/<suborder_no>', methods=['GET', 'POST'])
def status_change(suborder_no):
    """
    GET: {suborder_no}; returns {suborder_no, current_status}, 200
    POST: {suborder_no, new_status, comment}

    Status Table
    - ID - Integer
    - Status - ENUM
        1. Received || Set to this by default
        2. Processing
            a)Found
            b)Printed
        3. Mailed/Pickup
        4. Not_Found
           a)Letter_generated
           b)Undeliverable - Cant move down the line
        5. Done - End of status changes
    :return: {status_id, suborder_no, status, comment}, 201
    """

    if request.method == 'POST':  # Means that something was passed from the front
        # curr_status = str(request.form["status"])
        json = request.get_json(force=True)
        comment = json.get("comment")
        new_status = json.get("new_status")

        """
            POST: {suborder_no, new_status, comment};
            returns: {status_id, suborder_no, status, comment}, 201
        """
        update_status(suborder_no, comment, new_status)

    # return jsonify(current_status=curr_status, suborder_no=suborder_no, comment=comment, status_id=status_id)
    status = [status.serialize for status in StatusTracker.query.filter_by(suborder_no=int(suborder_no)).all()]
    return jsonify(status=status)


@api.route('/history/<int:suborder_no>', methods=['GET'])
def history(suborder_no):
    """
    GET: {suborder_no};
    :param suborder_no:
    :return: {suborder_no, previous value, new value, comment, date}, 200

    Look for all the rows with this suborder_no and list out the history for each one in Descending order
     also get the comment and date with these to send to the front
    """

    history = [status.serialize for status in StatusTracker.query.filter_by(suborder_no=int(suborder_no)).order_by(desc(StatusTracker.timestamp)).all()]

    return jsonify(history=history)


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    """
    :param order_id:
    :return: the orders with that specific client id that was passed
    """
    orders = [order.serialize for order in Order.query.filter_by(client_id=order_id).all()]

    if len(orders) == 0:
        abort(404)

    return jsonify(orders=orders)

@api.route('/print/<string:print_type>', methods=['POST'])
def print_order(type_):
    """
    Generate a PDF for a print operation.

    :param print_type: ('orders', 'small_labels', 'large_labels')
    """
    search_params = request.get_json(force=True)

    handler_for_type = {
        print_type.ORDERS: _print_orders,
        print_type.SMALL_LABELS: _print_small_labels,
        print_type.LARGE_LABELS: _print_large_labels
    }
    return handler_for_type[type_](search_params)


@api.route('/login', methods=['POST'])
def login():
    """
    Login a user through the API.

    :return: {user_id}, 200
    """
    user_info = request.get_json(force=True)

    successful_login = login_user(user_info['username'], user_info['password'])

    if successful_login:
        return jsonify(user_id="jocastillo@records.nyc.gov"), 200
    else:
        return jsonify(error="Invalid email or password for user account {}".format(user_info['username'])), 401
