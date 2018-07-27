from datetime import date
from flask import jsonify, abort, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from app.api_1_0 import api_1_0 as api
from app import db
from app.models.order_number_counter import OrderNumberCounter
from app.models.orders import Orders, Suborders
from app.models.customers import Customers
from app import db_utils
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
from app.db_utils import (create_object)
from app.constants import order_types
from app.models.photo import TaxPhoto,PhotoGallery
from app.models.property_card import PropertyCard

BIRTH_SEARCH = "Birth Search"
BIRTH_CERT = "Birth Cert"
MARRIAGE_SEARCH = "Marriage Search"
MARRIAGE_CERT = "Marriage Cert"
DEATH_SEARCH = "Death Search"
DEATH_CERT = "Death Cert"
TAX_PHOTO = "Tax Photo"
PHOTO_GALLERY = "Photo Gallery"
PROPERTY_CARD = "Property Card"

from app.api_1_0.utils import (
    update_status,
    get_orders_by_fields,
    _print_orders,
    _print_large_labels,
    _print_small_labels,
    update_tax_photo,
    generate_csv
)
from app.constants import (
    event_type
)
from app.constants import printing
from app.models import (
    Orders,
    TaxPhoto,
    Users,
    Events
)


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['GET', 'POST'])
@login_required
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with today's date.

    As a user, I want to be able to search for specific orders.

    GET {order_number, suborder_number, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in utils.py

    :return {orders, 200}
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        order_number = json.get("order_number")
        suborder_number = json.get("suborder_number")
        order_type = json.get("order_type")
        status = json.get("status")
        billing_name = json.get("billing_name")
        user = ''
        date_received_start = json.get("date_received_start")
        date_received_end = json.get("date_received_end")

        if not (order_number or suborder_number or billing_name) and not date_received_start:
            date_received_start = date.today()
        order_count, suborder_count, orders = get_orders_by_fields(order_number,
                                                                   suborder_number,
                                                                   order_type,
                                                                   status,
                                                                   billing_name,
                                                                   user,
                                                                   date_received_start,
                                                                   date_received_end)
        return jsonify(order_count=order_count,
                       suborder_count=suborder_count,
                       all_orders=orders), 200

    else:
        orders = []
        order_count = 0
        for order in Orders.query.filter(Orders.date_received == date.today()):
            order_count += 1
            for suborder in order.suborder:
                orders.append(suborder.serialize)
        return jsonify(order_count=order_count, suborder_count=len(orders), all_orders=orders), 200


@api.route('/orders/<doc_type>', methods=['GET'])
@login_required
def orders_doc(doc_type):
    """

    :param doc_type: document type ('csv' only)
    :return:
    """
    if doc_type.lower() == 'csv':
        url = generate_csv(request.args)
        return jsonify(url=url), 200


@api.route('/orders/new', methods=['POST'])
@login_required
def new_order():
    """
    :return:
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        add_description = json.get("addDescription")
        address_line_1 = json.get("addressLine1")
        address_line_2 = json.get("addressLine2")
        billing_name = json.get("billingName")
        block = json.get("block")
        borough = json.get("borough")
        bride_last_name = json.get("brideLastName")
        bride_first_name = json.get("brideFirstName")
        building_number = json.get("buildingNum")
        certified = json.get("certified")
        collection = json.get("collection")
        comment = json.get("comment")
        contact_number = json.get("contactNum")
        city = json.get("city")
        day = json.get("day")
        email = json.get("email")
        groom_last_name = json.get("groomLastName")
        groom_first_name = json.get("groomFirstName")
        instruction = json.get("instructions")
        img_id = json.get("imgId")
        img_title = json.get("imgTitle")
        letter = json.get("letter")
        lot = json.get("lot")
        mail = json.get("mail")
        marriage_place = json.get("marriagePlace")
        month = json.get("month")
        num_copies = json.get("numCopies")
        order_type = json.get("orderType")
        personal_use_agreement = json.get("personUseAgreement")
        phone = json.get("phone")
        print_size = json.get("printSize")
        roll = json.get("roll")
        state = json.get("state")
        status = json.get("status")
        street = json.get("street")
        years = json.get("year")
        zip_code = json.get("zipCode")

        year = datetime.datetime.now().strftime("%Y")
        today = datetime.datetime.today().strftime("%m/%d/%y")
        next_order_number = OrderNumberCounter.query.filter_by(year=year).one().next_order_number
        order_id = "EPAY-" + year + "-" + str(next_order_number)
        main_order = Orders(id=order_id,
                            date_submitted=today,
                            date_received=today,
                            confirmation_message="confirmation message",
                            client_data="client",
                            order_types=order_type,
                            multiple_items=True)
        # create_object(main_order)
        #
        customer = Customers(billing_name=billing_name,
                             email=email,
                             shipping_name=billing_name,
                             address_line_1=address_line_1,
                             address_line_2=address_line_2,
                             city=city,
                             state=state,
                             zip_code=zip_code,
                             phone=phone,
                             instructions=instruction,
                             order_number=main_order.id,
                             )
        # create_object(customer)
        #
        sub_order_number = Orders.query.filter_by(id=main_order.id).one().next_suborder_number
        sub_order_id = main_order.id + "-" + str(sub_order_number)
        sub_order = Suborders(id=sub_order_id,
                              client_id=customer.id,
                              order_type=order_type,
                              order_number=main_order.id,
                              _status=status
                              )
        # create_object(sub_order)
        if order_type == TaxPhoto:
            object = TaxPhoto(borough=None,
                              collection=collection,
                              roll=roll,
                              block=block,
                              lot=lot,
                              building_number=building_number,
                              street=street,
                              description=add_description,
                              mail=mail,
                              contact_number=contact_number
                              )
        elif order_type == PHOTO_GALLERY:
            object = PhotoGallery(image_id=img_id,
                                  description=img_title,
                                  add_description=add_description,
                                  size=print_size,
                                  num_copies=num_copies,
                                  mail=mail,
                                  contact_number=contact_number,
                                  personal_use_agreement=personal_use_agreement,
                                  comment=comment,
                                  suborder_number=sub_order.id
            )
        elif order_type == PROPERTY_CARD:
            object = PropertyCard(borough=borough,
                                  block=block,
                                  lot=lot,
                                  building_number=building_number,
                                  street=street,
                                  description=add_description,
                                  certified=certified,
                                  mail=mail,
                                  contact_number=contact_number,
                                  suborder_number=sub_order.id
                                  )
        # elif order_type == DEATH_CERT:



        print(order_type)

    return jsonify(), 200


@api.route('/status/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def status_change(suborder_number):
    """
    GET: {suborder_number}; returns {suborder_number, current_status}, 200
    POST: {suborder_number, new_status, comment}

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
    :return: {status_id, suborder_number, status, comment}, 201
    """
    if request.method == 'POST':
        json = request.get_json(force=True)
        comment = json.get("comment")
        new_status = json.get("new_status")

        """
            POST: {suborder_number, new_status, comment};
            returns: {status_id, suborder_number, status, comment}, 201
        """
        status_code = update_status(suborder_number, comment, new_status)
        return jsonify(status_code=status_code), 200


@api.route('/history/<string:suborder_number>', methods=['GET'])
@login_required
def history(suborder_number):
    """
    GET: {suborder_number};
    :param suborder_number:
    :return: {suborder_number, previous value, new value, comment, date}, 200

    Look for all the rows with this suborder_number and list out the history for each one in Descending order
     also get the comment and date with these to send to the front
    """
    # TODO: Events.type.in(..., event_type.UPDATE_TAX_PHOTO)
    status_history = [event.status_history for event in
                      Events.query.filter(Events.suborder_number == suborder_number,
                                          Events.type.in_(
                                              [event_type.UPDATE_STATUS, event_type.INITIAL_IMPORT])
                                          ).order_by(desc(Events.timestamp)).all()]

    return jsonify(history=status_history), 200


@api.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_single_order(order_id):
    """
    :param order_id:
    :return: the orders with that specific client id that was passed
    """
    orders = [order.serialize for order in Orders.query.filter_by(client_id=order_id).all()]

    if len(orders) == 0:
        abort(404)

    return jsonify(orders=orders), 200


@api.route('/tax_photo/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def tax_photo(suborder_number):
    if request.method == 'GET':
        t_photo = TaxPhoto.query.filter_by(suborder_number=suborder_number).one()
        return jsonify(block_no=t_photo.block,
                       lot_no=t_photo.lot,
                       roll_no=t_photo.roll), 200

    else:
        json = request.get_json(force=True)
        block_no = json.get("block_no")
        lot_no = json.get("lot_no")
        roll_no = json.get("roll_no")

        message = update_tax_photo(suborder_number, block_no, lot_no, roll_no)
        return jsonify(message=message), 200


@api.route('/print/<string:print_type>', methods=['POST'])
@login_required
def print_order(print_type):
    """
    Generate a PDF for a print operation.

    :param print_type: ('orders', 'small_labels', 'large_labels')
    """
    search_params = request.get_json(force=True)

    handler_for_type = {
        printing.ORDERS: _print_orders,
        printing.SMALL_LABELS: _print_small_labels,
        printing.LARGE_LABELS: _print_large_labels
    }

    url = handler_for_type[print_type](search_params)

    return jsonify({"url": url}), 200


@api.route('/login', methods=['POST'])
def login():
    """
    Login a user through the API.

    :return: {user_id}, 200
    """
    user_info = request.get_json(force=True)

    user = Users.query.filter_by(email=user_info['email']).one_or_none()

    if user is None:
        return jsonify(
            {
                "authenticated": False,
                "message": "Invalid username or password entered"
            }
        ), 401

    valid_password = user.verify_password(user_info['password'])

    if not valid_password:
        return jsonify(
            {
                "authenticated": False,
                "message": "Invalid username or password entered"
            }
        ), 401

    login_user(user)

    return jsonify(
        {
            "authenticated": True,
            "email": current_user.email
        }
    ), 200


@api.route('/logout', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    return jsonify({"authenticated": False}), 200
