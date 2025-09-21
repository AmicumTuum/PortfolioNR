select sum(quantity * price) as 'общая стоимость заказов' from orderlist ol, product p
where ol.idproduct = p.idproduct;

select idOrder as 'Номер заказа', SUM(quantity * price) as 'Сумма заказа' from OrderList ol, Product p
where ol.idProduct = p.idProduct
group by idOrder;

select * from product
where productname like 'kingstone%';

select * from Storage
where quantity = 1;

select MAX(orderDate) as 'Дата последнего заказа' from [Orders];

select * from [Orders]
where orderDate > '2021-01-01' and orderDate < '2021-04-15';

select SUM(quantity) as 'Количество товаров на складе' from Storage;

update Storage
set quantity = quantity+ 1--(quantity- 1)
from Storage
where idProduct = 2

select deliveryDate as 'Дата последней доставки на склад' from Storage 
order by deliveryDate desc;

select idEmployee as 'Сотрудник' from [Orders]
where (orderDate between '2021-01-01' and '2021-04-15')
group by idEmployee
having count(idOrder)>0;