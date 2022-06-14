create table user(
    ID			int NOT NULL AUTO_INCREMENT,
    name		varchar(64),
    password	varchar(8),
    address		varchar(100),
    admin       boolean DEFAULT false,
    regDate		TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    primary key (ID)
) ENGINE=INNODB;
create table manufacturer(
    name     	    varchar(64) not null,
    country		    varchar(32),
    location_count	int check (location_count>=0) DEFAULT 0,
    primary key (name)
) ENGINE=INNODB;
create table product(
    model           varchar(64) not null,
    name			varchar(64) DEFAULT '',
    maker           varchar(64),
    catagory        ENUM('laptop', 'storage', 'ram'),
    primary key (model),
    foreign key (maker) references manufacturer(name)
        on delete cascade
        on update cascade
) ENGINE=INNODB;
create table shop(
    name     		varchar(32) not null,
    address		    varchar(64) not null,
    phone			varchar(20) not null,
    opening_hour	varchar(20),
    primary key (name)
) ENGINE=INNODB;
create table purchase(
    ID			varchar(64),
    user_ID		int,
    product_ID	varchar(64),
    shop_name	varchar(64),
    address		varchar(100),
    price		int check (price > 0),
    order_date	date,
    primary key (ID),
    foreign key (user_ID) references user(ID)
        on delete cascade
        on update cascade,
    foreign key (shop_name) references shop(name)
        on delete cascade
        on update cascade,
    foreign key (product_ID) references product(model)
        on delete cascade
        on update cascade
) ENGINE=INNODB;
create table favors(
    ID          int NOT NULL AUTO_INCREMENT,         
    user_ID		int,
    product_ID	varchar(64),
    primary key (ID),
    foreign key (user_ID) references user(ID)
        on delete cascade
        on update cascade,
    foreign key (product_ID) references product(model)
        on delete cascade
        on update cascade
) ENGINE=INNODB;
create table ram(
    model		varchar(64),
    price		integer check (price > 0),
    ddr_type	ENUM('DDR2', 'DDR3', 'DDR4', 'DDR5', 'LPDDR4', 'DDR3L'),
    capacity	float check (capacity>0),
    ecc		    boolean DEFAULT false,
    warranty	varchar(10) not null DEFAULT 'life-long',
    rgb         boolean DEFAULT false,
    rate        integer DEFAULT 2666,
    primary key (model)
) ENGINE=INNODB;
create table storage(
    model		varchar(64),
    price		int check (price > 0),
    bus		    ENUM('SATA3', 'PCIe3', 'PCIe4'),
    media_type	ENUM('hdd', 'ssd'),
    formfactor	ENUM('2.5 inch', '3.5 inch','m.2 2280'),
    capacity	int check (capacity>0),
    portable	boolean DEFAULT false,
    warranty	varchar(10) not null DEFAULT 'life-long',
    read_speed  int check (read_speed>=0) DEFAULT 0,
    write_speed int check (write_speed>=0) DEFAULT 0,
    rpm         int DEFAULT 0,
    rgb         boolean DEFAULT false,
    primary key (model)
) ENGINE=INNODB;
create table laptop(
    model			varchar(64) not null,
    positioning	    ENUM('entry level', 'light gaming', 'pro gaming', 'professional', 'creator', 'bussiness'),
    price			int check (price > 0),
    series			varchar(64),
    os				varchar(64) not null,
    cpu			    varchar(64) not null,
    gpu			    varchar(64) DEFAULT '',
    vram            int DEFAULT 0,
    disk_capacity	float check (disk_capacity>0),
    ram             int check (ram>0),
    screen			float check (screen>0),
    dimension		varchar(64),
    resolution		varchar(20) DEFAULT '1920x1080',
    refreshRate 	int DEFAULT 60,
    weight			float not null,
    color			varchar(20) not null,
    warranty		varchar(20) not null DEFAULT '2-year',
    rgb             boolean DEFAULT false,
    primary key (model)
) ENGINE=INNODB;