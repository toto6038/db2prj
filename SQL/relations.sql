-- user
insert into user  values (NULL, 'Tommy', '12345', 'Taipei', true, NOW());
insert into user values (NULL, 'Howard', '14765', 'Tainan', true, NOW());
insert into user values (NULL, 'Fatsheep', 'ababa', 'Taipei', false, NOW());
-- storage
insert into storage values('z3', 1234, 'SATA3', 'ssd', '2.5 inch', 256, false, '1', 500, 300, 0, false);
-- ram
insert into ram values ('AD5U480008G-S', 1430, 'DDR5', 8, false, DEFAULT, DEFAULT, 4800);
insert into ram values ('PNY-16G-DDR4-2666', 1599, 'DDR4', 16, DEFAULT, DEFAULT, DEFAULT, 2666);
