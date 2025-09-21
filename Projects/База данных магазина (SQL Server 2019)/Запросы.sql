select sum(quantity * price) as '����� ��������� �������' from orderlist ol, product p
where ol.idproduct = p.idproduct;

select idOrder as '����� ������', SUM(quantity * price) as '����� ������' from OrderList ol, Product p
where ol.idProduct = p.idProduct
group by idOrder;

select * from product
where productname like 'kingstone%';

select * from Storage
where quantity = 1;

select MAX(orderDate) as '���� ���������� ������' from [Orders];

select * from [Orders]
where orderDate > '2021-01-01' and orderDate < '2021-04-15';

select SUM(quantity) as '���������� ������� �� ������' from Storage;

update Storage
set quantity = quantity+ 1--(quantity- 1)
from Storage
where idProduct = 2

select deliveryDate as '���� ��������� �������� �� �����' from Storage 
order by deliveryDate desc;

select idEmployee as '���������' from [Orders]
where (orderDate between '2021-01-01' and '2021-04-15')
group by idEmployee
having count(idOrder)>0;