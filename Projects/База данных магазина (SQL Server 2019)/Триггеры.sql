create trigger [dbo].[NotItemInStorage] on [Eldorado].[dbo].[OrderList]
after insert
as
begin
if exists (select s.quantity from Storage as s
		   Inner join Product p on p.idProduct = s.idProduct
		   Inner join OrderList ol on ol.idProduct = p.idProduct
		   where  ol.quantity> s.quantity or s.quantity = 0)
begin
rollback transaction raiserror('ƒанного количества товаров нет в наличии', 16, 20)
end
end