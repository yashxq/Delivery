import mysql.connector
from letsride.config import HOSTNAME, USERNAME, PASSWORD, DATABASE,SCHEMA, DEFAULT_START_DATE, DEFAULT_END_DATE
#mydb = mysql.connector.connect(host='localhost',user='root',password='123456',database="delivery" )
from rest_framework.response import Response
from django.http.response import JsonResponse
import datetime
from decryptor import PassKeyDecrypter


class generic_controller():
    @staticmethod
    def first_function(id):
        password_obj = PassKeyDecrypter()
        passw = password_obj.decrypt_password()

        mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
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
            password_obj = PassKeyDecrypter()
            passw = password_obj.decrypt_password()

            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
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
            password_obj = PassKeyDecrypter()
            passw = password_obj.decrypt_password()

            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
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

    def get_request_history(customer_id,start_date,end_date,date_order,status, asset_type):
        try:
            password_obj = PassKeyDecrypter()
            passw = password_obj.decrypt_password()

            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
            cur = mydb.cursor()

            if start_date=="":
                start_date = DEFAULT_START_DATE
            if end_date == "":
                end_date = DEFAULT_END_DATE

            if date_order not in ["desc","asc"]:
                date_order = "desc"

            select_statement = """select origin_address,delivery_address,pick_up_time,no_of_items,asset_type,asset_senstivity,receiver_details, accepter_details, order_status from {schema}.order_details where requester_id={customer_id} and (pick_up_time between '{start_date}' AND '{end_date}')""".format(schema=SCHEMA,start_date=start_date, end_date= end_date,customer_id=customer_id)

            if status != "":
                extra_status = """ and order_status = '{order_status}'""".format(order_status=status)
                select_statement+= extra_status
            if asset_type != "":
                extra_asset = """ and asset_type='{asset_type}'""".format(asset_type=asset_type)
                select_statement+= extra_asset
            select_statement += """ order by created_datetime {date_order}""".format(date_order=date_order)
            print(select_statement)
            cur.execute(select_statement)
            res = cur.fetchall()
            output=[]
            for u in res:
                t = datetime.datetime.strptime(str(u[2]), "%Y-%m-%d %H:%M:%S")
                n = datetime.datetime.now()
                status = u[8]
                if t<n :
                    status = 'Expired'
                output.append({ "from":u[0], "to":u[1], "date_and_time":u[2], "no_of_people":u[3], "asset_type":u[4], "asset_sensitivity":u[5], "whome_to_delivery":u[6],"accepted_person_details":u[7], "status":status })

            return JsonResponse(output, safe=False)
            

        except Exception as e:
            print(e)
            res = "Order Creation failed" +str(e)
            return JsonResponse(res, safe=False)

    def get_matched_delivery_options(customer_id):
        try:
            password_obj = PassKeyDecrypter()
            passw = password_obj.decrypt_password()

            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
            cur = mydb.cursor()

            # get request of only customer_id
            # for request that havent been assigned we want to see posible matches
            # no of items customer wants to move should be less then items rider is ready to carry
            ### --- IMP ---------
            # if request is flexible then we have buffer of 1 day up and down when package can be delivered. THis 1 day can be changed
            ## ------------------

            select_statement = """ select order_id, origin_address, delivery_address, receiver_details, no_of_items, asset_type, asset_senstivity, pick_up_flexible, rid.rider_id avaiable_rider,concat(firstName,' ',lastName) rider_name from {schema}.order_details ordl
           inner join delivery.rider_info rid on ordl.origin_address=rid.source_address and ordl.delivery_address=rid.destination_address 
           where ordl.rider_id = 0 and requester_id={customer_id} and no_of_items <= asset_quantity and 
           case when pick_up_flexible='yes' then ordl.pick_up_time between date_sub(rid.movement_date, interval 1 Day) and date_add(rid.movement_date, interval 1 Day) else ordl.pick_up_time = rid.movement_date end""".format(schema=SCHEMA,customer_id=customer_id)
            cur.execute(select_statement)
            res = cur.fetchall()
            output=[]
            for u in res:
                output.append({"order_id":u[0], "from":u[1],"to":u[2],"whome_to_deliver":u[3], "no_of_people": u[4], "asset_type":u[5], "asset_senstivity": u[6], "rider_id":u[8], "rider_name": u[9]})

            if len(output)==0:
                return JsonResponse("Sorry could not get matching details all your requests", safe=False)

            return JsonResponse(output, safe=False)

        except Exception as e:
            print(e)
            res = "Order Creation failed" +str(e)
            return JsonResponse(res, safe=False)

    def assign_rider_to_request(order_id,rider_id):
        try:
            password_obj = PassKeyDecrypter()
            passw = password_obj.decrypt_password()

            mydb = mysql.connector.connect(host=HOSTNAME,user=USERNAME,password=passw,database=DATABASE, auth_plugin='mysql_native_password')
            cur = mydb.cursor()

            update_statement = """update {schema}.order_details set rider_id={rider_id} where order_id={order_id}""".format(schema=SCHEMA,rider_id=rider_id,order_id=order_id)

            cur.execute(update_statement)
            mydb.commit()
            

            return JsonResponse("Delivery Assigned Succesfully", safe=False)

        except Exception as e:
            print(e)
            res = "Order Creation failed" +str(e)
            return JsonResponse(res, safe=False)







