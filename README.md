
# Assessment for SastaTicket

## Setting Up

To run this assessment, simply run:

```docker
docker compose up
```

I have also created 2 seeder scripts for you to seed products and users in the system. Go into the execution shell of the django container and run:

```python
python manage.py seed_products
```
This will create some products. Now Run:

```python
python manage.py seed_users
```
This will create 3 users, 2 of them regulars and 1 of them being superadmin.

1.  { "username": "adminuser", "email": "adminuser@gmail.com",
"password": "adminuserpasswordprotected"}

2.  { "username": "usera", "email": "usera@gmail.com",
"password": "userapasswordprotected"}

3.  { "username": "userb",  "email": "userb@gmail.com",
 "password": "userbpasswordprotected"}



## APIs
Now the main APIs in the system are:

### Authentication

1. 127.0.0.1:8000/auth/login/ (POST)

{"email": "the email" , "password": "the password"}

** The will return the token which needs to be sent in headers of the authenticated requests  as Authorization : Token {token} **

2. 127.0.0.1:8000/auth/register/ (POST)

{"email": "the email" , "password": "the password", "username":"the username"}

3. 127.0.0.1:8000/auth/logout/ (POST)


### Products

1. 127.0.0.1:8000/product/all/  (GET)


### Users

1. 127.0.0.1:8000/user/all/  (GET)
Only accessible by super admin


2. 127.0.0.1:8000/user/me/  (GET)
My info


### Orders

1. 127.0.0.1/order/order/  (GET)

Get all your created orders

2. 127.0.0.1:8000/order/order/{order_id}/  (GET)

Get order specified by order id if it is your , otherwise will receive 404.

3. 127.0.0.1:8000/order/order/   (POST)

To create order send the body with list of product_ids and the respective count of the products to order as below example:

{"requests":[{"product_id":"3f1b4c27-65d5-480e-acc9-7991c4d396c2", "quantity":1},{"product_id":"4d499f14-d23d-4a3e-8b27-27e8bfbabcbb", "quantity":3}]}


4. 127.0.0.1:8000/order/order/{order_id}/  (DELETE)

Delete any specific order, a user can delete only his orders


5. 127.0.0.1:8000/order/order/{order_id}/  (PUT)

If a user wants to update the order, the body would be similar to the body of create call , with the updated requests of products. example

{"requests":[{"product_id":"3f1b4c27-65d5-480e-acc9-7991c4d396c2", "quantity":1},{"product_id":"4d499f14-d23d-4a3e-8b27-27e8bfbabcbb", "quantity":3}]}

It will update the quantity numbers of products present in the order if the product is present in the order , otherwise would add the product into the order. Would remove the products from order not present in the request. It is the PUT call that accepts the updated requested products in the order.


6. 127.0.0.1:8000/order/ordersfetch?emails=    (GET)

Only accessible by super admin. Emails need to be sent in the query of the GET call to receive orders created by users having the queried emails. exmaple

127.0.0.1:8000/order/ordersfetch?emails=usera@gmail.com,userb@gmail.com



