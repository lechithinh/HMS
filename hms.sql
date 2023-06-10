CREATE database IF NOT EXISTS HMS;

use hms;


DROP TABLE IF EXISTS room;
CREATE TABLE `Room`(
	room_id int NOT NULL AUTO_INCREMENT,
    room_name varchar(45) DEFAULT NULL,
    floor int DEFAULT NULL,
    room_type varchar(45) DEFAULT NULL,
    room_price int DEFAULT NULL,
    room_beds int DEFAULT NULL,
    max_people int DEFAULT NULL,
    `status` varchar(45) DEFAULT NULL,
    isActive varchar(45) DEFAULT 'TRUE',
    created_at datetime default current_timestamp(),
    primary key(room_id)
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS Guest;
CREATE TABLE `Guest`(
	guest_id int NOT NULL AUTO_INCREMENT,
    guest_name varchar(45) DEFAULT NULL,
    phone_number varchar(45) DEFAULT NULL unique,
    address varchar(100) DEFAULT NULL,
    date_of_birth date DEFAULT NULL,
	created_at datetime default current_timestamp(),
    modified_at datetime default current_timestamp(),
    primary key(guest_id)
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS Inventory;
CREATE TABLE `Inventory`(
	item_id int NOT NULL AUTO_INCREMENT,
    item_name varchar(50) DEFAULT NULL,
    price int DEFAULT NULL,
    total int DEFAULT NULL,
    remain int DEFAULT NULL,
    created_at datetime default current_timestamp(),
    isActive varchar(45) DEFAULT 'TRUE',
    primary key(item_id)
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;



DROP TABLE IF EXISTS Staff;
CREATE TABLE `Staff`(
	staff_id int NOT NULL AUTO_INCREMENT,
    staff_name varchar(45) DEFAULT NULL,
    phone_number varchar(45) DEFAULT NULL,
    username varchar(100) DEFAULT NULL,
    address varchar(100) DEFAULT NULL,
    date_of_birth date DEFAULT NULL,
    `role` varchar(45) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    isActive varchar(45) default 'TRUE',
	created_at datetime default current_timestamp(),
    primary key(staff_id)
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS Booking;
CREATE TABLE Booking
(
	booking_id int not null auto_increment,
    room_id int not null,
	checkin_date datetime DEFAULT current_timestamp(),
    checkout_date datetime DEFAULT current_timestamp(),
    num_adult int default null,
    num_child int default null,
    isClose varchar(45) DEFAULT 'FALSE',
    primary key(booking_id),
    CONSTRAINT FK_Booking_Room FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;



DROP TABLE IF EXISTS booking_guest;
CREATE TABLE Booking_guest
(
	booking_id int not null,
    guest_id int not null,
	primary key(booking_id,guest_id),
    CONSTRAINT FK_BookingGuest_Booking FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE,
    CONSTRAINT FK_BookingGuest_Guest FOREIGN KEY (guest_id) REFERENCES Guest(guest_id) ON DELETE CASCADE
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Order`;
CREATE TABLE `Order`(
	booking_id int NOT NULL,
    item_id int NOT NULL,
    amount int DEFAULT NULL,
    total_price int DEFAULT NULL,
	created_at datetime default current_timestamp(),
    primary key(booking_id, item_id),
    CONSTRAINT FK_Order_Booking FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE,
    CONSTRAINT FK_Order_Inventory FOREIGN KEY(item_id) REFERENCES Inventory(item_id) ON DELETE CASCADE
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS Bill;
CREATE TABLE `Bill`(
	bill_id int NOT NULL AUTO_INCREMENT,
    booking_id int not null,
    room_id int NOT NULL,
    staff_id int NOT NULL,
    total_price int DEFAULT NULL,
    primary key(bill_id),
    created_at datetime default current_timestamp(),
    CONSTRAINT FK_Bill_Room FOREIGN KEY(room_id) REFERENCES Room(room_id) ON DELETE CASCADE,
    CONSTRAINT FK_Bill_Staff FOREIGN KEY(staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE,
    CONSTRAINT FK_Bill_Booking FOREIGN KEY(booking_id) references Booking(booking_id) ON DELETE cascade
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

#Only insert this 
insert into staff(staff_name, phone_number, username, address, date_of_birth, `role`, `password`) values
('Huynh Thien', 0832244567, 'huynhcongthien', 'Long an', '2003-5-28', 'Staff', '$2b$12$6nf/QuObvzgu50.d/pmUse1Go4aU6ToRpyfkWCnWN8l0ghIXgRbPK'),
('Nguyen Minh Tri', 083776543, 'nguyenminhtri', 'Bien Hoa', '2003-6-29', 'Manager', '$2b$12$4LDW4JVt7HP5nLZzb3ImWenAFesqwCCgX0OaY5ZOnB4dKFf8ACTMy'),
('Le Chi Thinh', 083772543, 'lechithinh', 'Ca Mau', '2003-5-12', 'Owner', '$2b$12$qhYvMNel/QlNYlV9PgHVe.tkokxmTzXBxpRAyYle.10G1xmlCbrH.');





INSERT into room (room_name,floor,room_type,room_price,room_beds,max_people,`status`,isActive) values 
('Room1',	1,	'NORMAL'	,200,	1,	2,	'Occupied',	'TRUE'),
('Room2',	1,	'NORMAL'	,200,	1,	2,	'Available','TRUE'),
('Room3',	2,	'VIP'	,	400,	2,	4,	'Available','TRUE'),
('Room4',	2	,'VIP'	,	400,	2,	4,	'Occupied',	'TRUE');

INSERT INTO Guest (guest_name, phone_number, address, date_of_birth) values
('Le Thinh', 45621248, 'Ca Mau', '2003-05-12'),
('Cong Thien', 431566443, 'Ho Chi Minh', '2003-12-6'),
('Minh Tri', 123456789, 'Lam Dong', '2003-7-12');



INSERT INTO Staff(staff_name, phone_number, username, address, date_of_birth, role, Password) values
('Nguyen Van A', 822098222, 'vana', 'Ca Mau', '1990-5-12', 'Manager', 'X'),
('Le Van Chi', 822098211, 'levanchi', 'Long An', '2003-5-13', 'Staff', 'T'),
('Tran Van Anh', 822098342, 'tranvananh', 'Bien Hoa', '2000-3-28', 'Staff', 'Y'),
('Pham Van Em', 822098102, 'phanvanem', 'Ha Giang', '1999-9-19', 'Staff', 'Z'),
('Le Chi Thinh', 822043153, 'lechithinh', 'Ca Mau', '2000-5-12', 'Owner', 'T');

INSERT INTO hms.inventory(item_name, price , total, remain) values
('water', 5, 20, 18),
('coca', 10, 20, 20),
('pessi', 10, 20, 20);

insert into hms.order (booking_id,item_id,Amount,Total_price) values
(2, 1, 2, 10),
(2, 2, 2, 20),
(1, 1, 3, 15);

INSERT INTO booking (room_id, checkin_date, checkout_date, isClose) values 
(1,	'2023-06-04',	'2023-06-10',	'FALSE'),
(4,	'2023-05-05',	'2023-05-15',	'FALSE'),
(4, '2023-04-04', '2023-05-04', 'TRUE');

INSERT INTO booking_guest values 
(1,	3),
(2	,2),
(2, 1);



    

