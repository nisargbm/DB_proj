CREATE TABLE IF NOT EXISTS User(
user_id varchar(255) NOT NULL ,
password varchar(255) NOT NULL,
email_id varchar(255) NOT NULL UNIQUE,
department varchar(255) NOT NULL,
PRIMARY KEY(user_id)
);
ALTER TABLE User ADD CONSTRAINT email CHECK(email_id LIKE '%_@_%_.__%');
CREATE TABLE Name(
First_name varchar(255) NOT NULL,
CONSTRAINT fn CHECK (First_name NOT LIKE '%[^0-9]%'),
Middle_name varchar(255) NOT NULL,
CONSTRAINT mn CHECK (Middle_name NOT LIKE '%[^0-9]%'),
Last_name varchar(255) NOT NULL,
CONSTRAINT ln CHECK (Last_name NOT LIKE '%[^0-9]%'),
user_id varchar(255) NULL,
CONSTRAINT fr1 FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE Mobile(
mobile_no int NOT NULL UNIQUE,
CONSTRAINT number CHECK (mobile_no LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' AND LENGTH(mobile_no)=10),
user_id varchar(255) NULL
);
ALTER TABLE Mobile ADD CONSTRAINT fr2 FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE Document_details(
doc_id int ,
subject varchar(255) NOT NULL,
number_of_documents int NOT NULL,
CHECK (number_of_documents >=1),
details varchar (255),
organisation varchar (255) NOT NULL,
PRIMARY KEY (doc_id)
);

CREATE TABLE Document(
sr_no int AUTOINCREMENT=1,
doc_id int NOT NULL ,
Date_of_receipt datetime DEFAULT NOW(),
sender varchar (255) NOT NULL,
receiver varchar (255) NULL,
FOREIGN KEY (doc_id) REFERENCES Document_details(doc_id) ON DELETE CASCADE ON UPDATE CASCADE
PRIMARY KEY (sr_no)
);

CREATE TABLE Inward(
inward_id int AUTOINCREMENT=1,
place_of_receiving varchar(255) NOT NULL,
doc_id int NOT NULL,
FOREIGN KEY (doc_id) REFERENCES Document_details(doc_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (inward_id)
);

CREATE TABLE Outward(
outward_id int AUTOINCREMENT=1 ,
sending_place varchar(255) NOT NULL,
to_whom_addressed varchar(255) NOT NULL,
doc_id int NOT NULL,
FOREIGN KEY (doc_id) REFERENCES Document_details(doc_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (outward_id)
);

CREATE TABLE Postal_charges(
post_id int AUTOINCREMENT=1,
type_of_post varchar(50) NULL,
estimated_cost int NOT NULL,
outward_id int NOT NULL,
FOREIGN KEY (outward_id) REFERENCES Outward(outward_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (post_id)
);

CREATE TABLE Process(
user_id varchar (255) NOT NULL,
doc_id int NOT NULL ,
movement_date date NOT NULL,
status varchar(50) DEFAULT 'PENDING'
comment varchar(255) NULL DEFAULT 'NO COMMENTS',
FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (doc_id) REFERENCES Document(doc_id) ON DELETE CASCADE ON UPDATE CASCADE,
);
