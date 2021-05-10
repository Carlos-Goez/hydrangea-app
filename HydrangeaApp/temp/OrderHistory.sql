create table OrderHistory
(
	Order_ID INTEGER
		primary key,
	Order_Status VARCHAR(20),
	Username VARCHAR(30),
	Creation_Date DATETIME,
	Production_Date DATETIME,
	Finish_Date DATETIME,
	Quantity_Mini INTEGER,
	Quantity_Select INTEGER,
	Quantity_Blue INTEGER,
	Outstanding_Mini INTEGER,
	Outstanding_Select INTEGER,
	Outstanding_Blue INTEGER,
	Packing_Position INTEGER,
	Size_Box VARCHAR(20)
);

