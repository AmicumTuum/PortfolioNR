create function [dbo].[productNameByCost]
(@price int)
returns @Result table 
(idProduct int,
idType int,
idWaranry int,
productName varchar(30),
price int)
begin
insert @Result
select *
from Product
where @price > price 
return
end

select * from productNameByCost(25000)


create FUNCTION [dbo].[getFIEmployee] (@IdEmployee int)
RETURNS varchar(25)
AS
BEGIN
DECLARE @result varchar(25)
SET @result = 'NULL'
SELECT @result = SUBSTRING(LName, 1, 1) + '. ' + FName
FROM Staff
WHERE idEmployee = @IdEmployee
RETURN @result
END

select dbo.getFIEmployee(4) 'Инициалы сотрудника'


create function [dbo].[productNameByPrice](@name int)
returns varchar(25)
Begin
declare @result varchar(25)
select @result = productName from Product p
where @name = p.price
return @result
end

select dbo.productNameByPrice(129999) as 'Товар заданной цены'