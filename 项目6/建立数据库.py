creat database if not exit house_analysis default charest utf8mb4;
use house_analysis;

creat table houses(
id int auto_increment primary key,
community varchar(100),
total_price decimal(10,2)comment'总价(万元)',
square decimal(8,2)comment'面积(平米)',
unit_price decimal(10,2)comment'单价(元/平米)',
living_room int comment'客厅数',
drawing_room int comment '卧室数',
floor_type VARCHAR(10) COMMENT '楼层类型（高/中/低）',
total_floor INT COMMENT '总楼层数',
construction_year INT COMMENT '建筑年代',
district VARCHAR(30) COMMENT '区域',
near_subway tinyint comment'1是0否',
followers INT COMMENT '关注人数'
);