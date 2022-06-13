-- user
insert into user values ('123456', 'Tommy', '12345', 'Taipei', true, NOW());
insert into user values ('121216', 'Howard', '14765', 'Tainan', true, NOW());
insert into user values ('889966', 'Fatsheep', 'ababa', 'Taipei', false, NOW());
-- storage
insert into storage values('z3', 1234, 'SATA3', 'ssd', '2.5 inch', 256, false, '1', 500, 300, 0, false);
-- ram
insert into ram values ('AD5U480008G-S', 1430, 'DDR5', 8, false, DEFAULT, DEFAULT, 4800);
insert into ram values ('PNY-16G-DDR4-2666', 1599, 'DDR4', 16, DEFAULT, DEFAULT, DEFAULT, 2666);
-- laptop
insert into laptop values ('15s-eq2173AU', 'entry level', 15888, '', 'Windows 11', 'Ryzen 3-5300U', DEFAULT, DEFAULT, 256, 8, 15.6, '358.5x242x17.9', DEFAULT, DEFAULT, 1.69, 'white', '1-year', DEFAULT);
-- manufacturer
insert into manufacturer values ('ASUS', 'Taiwan', 1);