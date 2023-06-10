CREATE database IF NOT EXISTS HMS;

use hms;
select * from staff

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
    primary key(item_id)
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Order`;

DROP TABLE IF EXISTS Staff;
CREATE TABLE `Staff`(
	staff_id int NOT NULL AUTO_INCREMENT,
    staff_name varchar(45) DEFAULT NULL,
    phone_number int DEFAULT NULL,
    username varchar(100) DEFAULT NULL,
    address varchar(100) DEFAULT NULL,
    date_of_birth date DEFAULT NULL,
    `role` varchar(45) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    isActive varchar(45) default 'TRUE',
	created_at datetime default current_timestamp(),
    primary key(staff_id)
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

select * from bill
DROP TABLE IF EXISTS Booking;
CREATE TABLE Booking
(
	booking_id int not null auto_increment,
    room_id int not null,
	checkin_date datetime DEFAULT current_timestamp(),
    checkout_date datetime DEFAULT current_timestamp(),
    isClose varchar(45) DEFAULT 'FALSE',
    primary key(booking_id),
    CONSTRAINT FK_Booking_Room FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

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


-- INSERT INTO `order`(booking_id, item_id, amount, total_price)
-- VALUES (1, 2, 5, 15)
-- ON DUPLICATE KEY UPDATE
--     amount = 5,
--     total_price = 5 * 15


DROP TABLE IF EXISTS booking_guest;
CREATE TABLE Booking_guest
(
	booking_id int not null,
    guest_id int not null,
	primary key(booking_id,guest_id),
    CONSTRAINT FK_BookingGuest_Booking FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE,
    CONSTRAINT FK_BookingGuest_Guest FOREIGN KEY (guest_id) REFERENCES Guest(guest_id) ON DELETE CASCADE
)engine=InnoDB auto_increment=1 DEFAULT CHARSET=utf8mb4 collate=utf8mb4_0900_ai_ci;

INSERT into room (room_name,floor,room_type,room_price,room_beds,max_people,`status`,isActive) values 
('Room1',	1,	'NORMAL'	,200,	1,	2,	'Occupied',	'TRUE'),
('Room2',	1,	'NORMAL'	,200,	1,	2,	'Available','TRUE'),
('Room3',	2,	'VIP'	,	400,	2,	4,	'Available','TRUE'),
('Room4',	2	,'VIP'	,	400,	2,	4,	'Occupied',	'TRUE');

INSERT INTO Guest (guest_name, phone_number, address, date_of_birth) values
('Le Thinh', 45621248, 'Ca Mau', '2003-05-12'),
('Cong Thien', 431566443, 'Ho Chi Minh', '2003-12-6'),
('Minh Tri', 123456789, 'Lam Dong', '2003-7-12');

insert into staff(staff_name, phone_number, username, address, date_of_birth, `role`, `password`) values
('Huynh Thien', 0832244567, 'huynhcongthien', 'Long an', '2003-5-28', 'Staff', '456'),
('Nguyen Minh Tri', 083776543, 'nguyenminhtri', 'Bien Hoa', '2003-6-29', 'Manager', '789'),
('Le Chi Thinh', 083772543, 'lechithinh', 'Ca Mau', '2003-5-12', 'Owner', '123');

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


ALTER TABLE room AUTO_INCREMENT=1;
select * from room ;

select * from guest ;
select * from inventory ;
select * from booking;
select * from booking_guest;

select item_name, amount
from `order` join `inventory`
on `order`.item_id = inventory.item_id join booking 
on booking.booking_id = `order`.booking_id
where room_id = 4 and isClose = 'FALSE' and item_name ='pessi'

select * from staff;
select * from `order`;
update room
set `status` = "Occupied"
where room_id = 1;




-- -------- CHECK IN ------------
-- INSERT vô tbl guest khi check-in
# 2 TH: nếu như thông tin guest đã có trong table guest thì chọn lại guest_id cũ, nếu như chưa có thì thêm mới
INSERT INTO guest (guest_name, phone_number, address, date_of_birth)
VALUES ('Minh Tri', 123456789,'bien hoa','2003-07-12')
ON DUPLICATE KEY UPDATE 
modified_at = current_timestamp();

-- UPDATE trạng thái room khi check-in
UPDATE room
SET status = 'occupied'
WHERE room_id = idx  -- idx: room_id của room được chọn để check-in

-- Lấy guest_id của các guest thuộc room được chọn
SELECT guest_id
FROM guest
ORDER BY modified_at DESC
LIMIT -- số lượng guest muốn lấy guest_id ;


-- INSERT booking table
INSERT INTO booking values (room_id, checkin_date, checkout_date, isClose) values (%s,%s,%s.%s)

/*
-- INSERT vô tbl staying-bridge
INSERT INTO staying-bridge values -- (room_id, guest_id, checkin_date, checkout_date, false)
*/


-- INSERT order lúc check-in
INSERT INTO	order (booking_id,item_id,amount,total_price) values ($,$,$,$),($,$,$,$),($,$,$,$)


-- -------- CHECKOUT ------------
-- UPDATE trạng thái room khi check out
UPDATE room
SET status = 'Available'
WHERE room_id = idx -- idx: room_id của room được chọn để check-out

-- lấy thông tin của các guest thuộc room đó và view lên web
/*# cach 1:
SELECT 
FROM guest, staying-bridge
WHERE guest.guest_id = staying-bridge.guest_id AND room_id = 11 AND isClose = 'FALSE' ;

# cach 2:

select *
from guest inner join (
select guest_id
from staying-bridge
where room_id = 11 AND isClose = 'FALSE' )  as tbl1
on guest.guest_id = tbl1.guest_id;
*/
select guest.guest_id, guest_name, phone_number, address, date_of_birth, created_at, modified_at
from (
	select * 
	from booking 
	where room_id = 4 and isClose = "FALSE" ) table1
inner join booking_guest
on table1.booking_id = booking_guest.booking_id
inner join guest
on booking_guest.guest_id = guest.guest_id;




    
-- UPDATE isClose 
UPDATE booking
SET isClose = 'TRUE'
WHERE room_id = idx AND isClose = 'FALSE'; -- idx: room_id của room được chọn để check-out

-- UPDATE guest
select * from guest;
select guest_id
from booking bk join booking_guest bg
on bk.booking_id = bg.booking_id
where room_id = 4;

UPDATE guest 
SET guest_name = 'Van A', phone_number = 10218308, address = 'Tan Thanh', date_of_birth = '2003-05-05'
WHERE guest_id = 5

-- ------------------- BILL --------------------

-- tính total_price của bill
-- get booking id
select id from inventory;
select * from `inventory`;
select booking_id
from room join booking
on room.room_id = booking.booking_id
where booking.room_id = 4 and booking.isClose = 'False';


-- lay booking_id cua phong 

SELECT checkin_date, checkout_date, room_type, room_beds, room_price, total_price, TIMESTAMPDIFF(Day,checkin_date,checkout_date) as remainday,  TIMESTAMPDIFF(Day,checkin_date,checkout_date) * room_price + total_price as bill_price
FROM (SELECT booking_id, room.room_id, checkin_date, checkout_date, room_type, room_beds, room_price
	FROM booking inner join room
	on booking.room_id = room.room_id
	WHERE booking_id = 2 ) as table1
inner join 
	(SELECT booking_id, sum(total_price) as total_price
    FROM `order`
    WHERE booking_id = 2 ) as table2
ON table1.booking_id = table2.booking_id



select * from guest;
-- INSERT 
INSERT INTO bill (room_id,staff_id,total_price) values (%s,%s,%s)

-- ------------------- ORDER --------------------

-- INSERT
	# lấy ra id và price của item có name = (list các món order)
	SELECT item_id, price
	FROM inventory
	WHERE item_name =  # tên của vật phẩm trong danh sách order

	# cập nhật inventory 
	UPDATE inventory
	SET remain = remain - Amount # Amount là giá trị của biến st.slider trong code
	WHERE item_id = item_id
select * from `order`

	# với từng vật phẩm mà có số lượng lớn hơn 0 được lưu trong 1 list, ta lấy số lượng * price
	INSERT INTO order (room_id,item_id,Amount,Total_price) 
	values ( # room id: idx của room order, item_id: kết quả của câu lệnh sql trên, amount: giá trị của biến st.slider trong code, total_price: tính bằng cách lấy price* amount, tính ở trong code)


-- UPDATE

	SELECT item_id, price
	FROM inventory
	WHERE item_name = # tên của vật phẩm trong danh sách order


	# kiểm tra món item khách order đã có trong bảng order chưa
	SELECT count(item_id) cnt_item # lấy ra số lượng của item khách order 
	FROM order
	WHERE item_id = /* cai j do / and room_id = / cai j do / and / 1 điều kiện vd như isclose */

	# có 2 TH khi cập nhật order:
	## TH1: khi item đó không có trong order thì insert vô như bình thường
		INSERT INTO order (room_id,item_id,Amount,Total_price) 
		values (%s, %s, %s, %s)
		
	## TH2: khi item đó có trong order thì cộng dồn amount và tính lại total_price
		UPDATE order
		SET amount = amount + Amount # amount: số lượng cũ, Amount: số lượng mới, được lưu trong biến st.slider
		, Total_price = Total_price + Amount*price # price: đã lấy ở trên
		WHERE item_id = /* cai j do / and room_id = / cai j do / and / 1 điều kiện vd như isclose */

	# cập nhật inventory 
	UPDATE inventory
	SET remain = remain - Amount # amount là giá trị của biến st.slider trong code
	WHERE item_id = item_id


	#  lấy thông tin order của phòng đã đặt
	SELECT item_id, amount, total_price 
	FROM order
	WHERE booking_id = booking_id # booking_id của phòng hiện tại đang chọn
-- --------------------- ROOM -------------------
-- INSERT 
INSERT INTO room (room_name,floor,room_type,room_price,room_beds,max_people,`status`,isActive) values (%s, %s, %s, %s,%s, %s, %s, %s)

-- UPDATE
UPDATE room
SET room_name = %s and floor = %s and room_type = %s and room_price = %s and room_beds  = %s and max_people  = %s and status = %s and isActive = %s
WHERE room_id = idx



-- --------------------- INVENTORY --------------
-- add new item






-- -------------------------------------------------
select * from Order;
DROP TRIGGER IF EXISTS after_insert_order;

	CREATE TRIGGER after_insert_order
    AFTER INSERT ON Order
    FOR EACH ROW
     UPDATE Inventory
	SET remain = remain - NEW.amount
    where item_id = NEW.item_id

select * from Order;
select * from Inventory;
insert into `Order`(room_id,item_id,Amount,Total_price) values
(12, 14, 3, 15);



DROP TRIGGER IF EXISTS after_insert_staying_status;

	CREATE TRIGGER after_insert_staying_status
    AFTER INSERT ON staying-bridge
    FOR EACH ROW
     UPDATE room
	SET status = 'Occupied' 
    where room_id = NEW.room_id





-- -------------------------- BOOKING ----------------
-- lấy booking_id từ room_id
SELECT booking_id
FROM booking
WHERE room_id = idx and isClose = FALSE;


-- -------------------------- LOG IN -----------------
SELECT staff_id, staff_name, username, password
FROM staff;

SELECT staff_name,	phone_number,	username,	address,	date_of_birth,	role
FROM staff
WHERE staff_id = %s;
select * from room;
update room
set room_beds = '2'
where room_id = 4

select *
from staff 
where username = 'huynhcongthien' and password = '456';
