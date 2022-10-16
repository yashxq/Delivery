import mysql.connector
from letsride.config import HOSTNAME, USERNAME, PASSWORD, DATABASE,SCHEMA
#mydb = mysql.connector.connect(host='localhost',user='root',password='123456',database="delivery" )
from rest_framework.response import Response
from django.http.response import JsonResponse


class generic_controller():
    @staticmethod
    def first_function(id):
        mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,database=DATABASE, auth_plugin='mysql_native_password')
        cur = mydb.cursor()

        select_statement = """select * from {schema}.rider_info""".format(schema=SCHEMA)
        cur.execute(select_statement)
        res = cur.fetchall()
        output=[]
        for x in res:
            output.append({"rider_id":x[0],"lastName":x[1],"firstName":x[2],"travel_medium":x[3],"updated_dattime":x[4]})
        return JsonResponse(output, safe=False)

    @staticmethod
    def creater_order(data):
        try:
            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,database=DATABASE, auth_plugin='mysql_native_password')
            cur = mydb.cursor()

            select_statement = """select max(order_id)+1 new_order_id from {schema}.order_details""".format(schema=SCHEMA)
            cur.execute(select_statement)
            res = cur.fetchall()
            new_order_id = 0
            for x in res:
                new_order_id = x[0]

            # This Entire Select can be removed but MySQL doesnt allow doesn’t allow updates to a table when you are also using that same table
            # THere is a work Around but will have to check it later

            insert_statement = """insert into {schema}.order_details values ({new_order_id},{requester_id}, 0, '{source_address}', '{destination_address}', '{receiver_details}', '', {no_of_items},  '{asset_type}', '{asset_senstivity}', '{pick_up_time}', '{pick_up_flexible}', 'PENDING', now(), now())""".format(schema=SCHEMA, requester_id=data['requester_id'], source_address=data['origin_address'],destination_address=data['delivery_address'], receiver_details=data['receiver_details'], no_of_items= data['no_of_items'], asset_type=data['asset_type'], asset_senstivity=data['asset_senstivity'],pick_up_time = data['pick_up_time'],pick_up_flexible=data['pick_up_flexible'],new_order_id=new_order_id )
            
            print(insert_statement)
            cur.execute(insert_statement)
            mydb.commit()

            return JsonResponse("Order Placed Succesfully", safe=False)
        except Exception as e:
            print(e)
            res = "Order Creation failed" +str(e)
            return JsonResponse(res, safe=False)

    def creater_travel_details(data):
        try:
            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=PASSWORD,database=DATABASE, auth_plugin='mysql_native_password')
            cur = mydb.cursor()

            select_statement = """select firstName,lastName from {schema}.customer_info where customer_id={customer_id}""".format(schema=SCHEMA,customer_id=data['customer_id'])
            cur.execute(select_statement)
            res = cur.fetchall()
            firstName = ''
            lastName = ''
            for x in res:
                firstName = x[0]
                lastName = x[1]

            insert_statement = """insert into {schema}.rider_info values ({customer_id}, '{lastName}', '{firstName}', '{travel_medium}','{source_address}','{destination_address}',{no_of_items},'{movement_date}','{flexible_timings}', now(), now())""".format(schema=SCHEMA, customer_id=data['customer_id'],lastName=lastName,firstName=firstName, travel_medium=data['travel_medium'], source_address=data['source_address'], destination_address=data['destination_address'], no_of_items=data['no_of_items'], movement_date = data['movement_date'], flexible_timings=data['flexible_timings'])

            print(insert_statement)
            cur.execute(insert_statement)
            mydb.commit()

            return JsonResponse("Ride Details Saved Succesfully", safe=False)

            #nkvn

        except Exception as e:
            print(e)
            res = "Order Creation failed" +str(e)
            return JsonResponse(res, safe=False)



