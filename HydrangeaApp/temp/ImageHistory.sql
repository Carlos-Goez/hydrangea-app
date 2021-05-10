create table ImageHistory
(
	Image_ID INTEGER
		primary key autoincrement,
	Order_ID INTEGER,
	File_Path_RGB VARCHAR(100),
	File_Path_NOIR VARCHAR(100),
	NOIR REAL,
	GCI REAL,
	Flower_Type VARCHAR(20),
	Capture_Date DATETIME
);

