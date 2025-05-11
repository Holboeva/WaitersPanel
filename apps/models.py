# from django.db import models

# class Staff(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     role = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Table(models.Model):
#     number = models.IntegerField(unique=True)
#     is_occupied = models.BooleanField(default=False)  
#     number_of_clients = models.IntegerField(default=0)  
#     apps = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"Table {self.number}"
    
# from django.db import models

# class Menu(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     category = models.CharField(max_length=50)  # e.g., 'meal' or 'drink'
#     description = models.TextField(blank=True)
#     image_url = models.URLField(max_length=500, blank=True)
#     is_available = models.BooleanField(default=True)
#     prep_time = models.IntegerField(default=0)  # in minutes
#     spicy_level = models.IntegerField(default=0)  # from 0 (none) to 5 (very spicy)
#     is_vegetarian = models.BooleanField(default=False)
#     rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('preparing', 'Preparing'),
#         ('served', 'Served'),
#         ('billed', 'Billed'),
#     ]
#     table = models.ForeignKey(Table, on_delete=models.CASCADE)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} - Table {self.table.number}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     note = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.quantity}x {self.menu.name} (Order #{self.order.id})"


from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Table(models.Model):
    number = models.IntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)
    number_of_clients = models.IntegerField(default=0)
    waiter = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Table {self.number}"


class Menu(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    prep_time = models.IntegerField(default=0)
    spicy_level = models.IntegerField(default=0)
    is_vegetarian = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('billed', 'Billed'),
    ]
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu.name} (Order #{self.order.id})"



class OrderHistory(models.Model):
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    order_details = models.JSONField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderHistory - Table {self.table.number} at {self.ordered_at.strftime('%Y-%m-%d %H:%M')}"
