CREATE TABLE delivery.rider_info (
    rider_id int NOT NULL AUTO_INCREMENT,
    lastName varchar(255) NOT NULL,
    firstName varchar(255),
    travel_medium varchar(255),
    source_address varchar(225),
    destination_address varchar(225),
    asset_quantity int,
    movement_date DATETIME(6),
    flexible_timings varchar(20),
    created_datetime timestamp,
    updated_dattime timestamp,
    PRIMARY KEY (rider_id)
);

CREATE TABLE delivery.customer_info (
    customer_id int NOT NULL AUTO_INCREMENT,
    lastName varchar(255) NOT NULL,
    firstName varchar(255),
    home_address varchar(500),
    created_datetime timestamp,
    updated_dattime timestamp,
    PRIMARY KEY (customer_id)
);

CREATE TABLE delivery.order_details (
    order_id int NOT NULL AUTO_INCREMENT,
    requester_id int,
    rider_id int,
    origin_address varchar(500),
    delivery_address varchar(500),
    receiver_details varchar(500),
    accepter_details varchar(500),
    no_of_items int,
    asset_type varchar(500),
    asset_senstivity varchar(500),
    pick_up_time DATETIME(6),
    pick_up_flexible varchar(20),
    order_status varchar(20),
    created_datetime timestamp,
    updated_dattime timestamp,
    PRIMARY KEY (order_id)
);

select * from delivery.rider_info;
insert into delivery.rider_info values (1, 'Kapoor', 'Sanjay', 'CAR','Paris','London',4,'2022-10-10 10:10:10','Yes', now(), now());

select * from delivery.customer_info;
insert into delivery.customer_info values (1, 'Kapoor', 'Arjun', 'Paris', now(), now());

select * from delivery.order_details;
insert into delivery.order_details values (1, 1, 1, 'Paris', 'London', 'Pankaj-8000080000',
'',3,'LAPTOP','NORMAL','2022-10-10 10:10:10','Yes','PENDING',now(),now());