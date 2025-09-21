create procedure [dbo].[OrdersById]
@idProduct int
as
select * from ([Orders] o
Inner join OrderList ol on ol.idOrder = o.idOrder)
Inner join Product p on p.idProduct = ol.idProduct
where @idProduct = p.idProduct
exec OrdersById 3;

create procedure [dbo].[CountStaffUp]
@print int out
as
set @print = (SELECT COUNT(*) FROM Staff s
where exists 
  (select idOrder
   from [Orders] ord
   where s.idEmployee = ord.idEmployee
  ))
return

declare @print int
exec dbo.CountStaffUp
@print = @print output
select @print ' оличество сотрудников, выполн€ющих работу'

create procedure [dbo].[getOrdersByDate]
as
select idOrder, idEmployee, orderDate
from [Orders]
where (orderDate <= '2021-02-28')
return;

exec getOrdersByDate
