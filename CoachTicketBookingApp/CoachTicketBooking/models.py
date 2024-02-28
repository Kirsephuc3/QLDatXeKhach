from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_date = models.DateField(auto_now_add=True, null=True)
    update_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    Role_choice = [
        ('admin', 'Amin'),
        ('ticket seller', 'Nhân Viên Bán Vé'),
        ('driver', 'Tài Xế'),
        ('user', 'Khách hàng')
    ]

    Gender_choice = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ]
    avatar = CloudinaryField('image', null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True, choices=Role_choice)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, choices=Gender_choice)
    address = models.CharField(max_length=255, null=True)


class Driver(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.license_number}"


# Tuyến xe
class Route(BaseModel):
    VIETNAM_PROVINCES = [
        ('AN_GIANG', 'An Giang'),
        ('BA_RIA_VUNG_TAU', 'Bà Rịa - Vũng Tàu'),
        ('BAC_LIEU', 'Bạc Liêu'),
        ('BAC_GIANG', 'Bắc Giang'),
        ('BAC_KAN', 'Bắc Kạn'),
        ('BAC_NINH', 'Bắc Ninh'),
        ('BEN_TRE', 'Bến Tre'),
        ('BINH_DUONG', 'Bình Dương'),
        ('BINH_DINH', 'Bình Định'),
        ('BINH_PHUOC', 'Bình Phước'),
        ('BINH_THUAN', 'Bình Thuận'),
        ('CA_MAU', 'Cà Mau'),
        ('CAO_BANG', 'Cao Bằng'),
        ('CAN_THO', 'Cần Thơ'),
        ('DA_NANG', 'Đà Nẵng'),
        ('DAK_LAK', 'Đắk Lắk'),
        ('DAK_NONG', 'Đắk Nông'),
        ('DIEN_BIEN', 'Điện Biên'),
        ('DONG_NAI', 'Đồng Nai'),
        ('DONG_THAP', 'Đồng Tháp'),
        ('GIA_LAI', 'Gia Lai'),
        ('HA_GIANG', 'Hà Giang'),
        ('HA_NAM', 'Hà Nam'),
        ('HA_NOI', 'Hà Nội'),
        ('HA_TINH', 'Hà Tĩnh'),
        ('HAI_DUONG', 'Hải Dương'),
        ('HAI_PHONG', 'Hải Phòng'),
        ('HAU_GIANG', 'Hậu Giang'),
        ('HOA_BINH', 'Hòa Bình'),
        ('HUNG_YEN', 'Hưng Yên'),
        ('KHANH_HOA', 'Khánh Hòa'),
        ('KIEN_GIANG', 'Kiên Giang'),
        ('KON_TUM', 'Kon Tum'),
        ('LAI_CHAU', 'Lai Châu'),
        ('LANG_SON', 'Lạng Sơn'),
        ('LAO_CAI', 'Lào Cai'),
        ('LAM_DONG', 'Lâm Đồng'),
        ('LONG_AN', 'Long An'),
        ('NAM_DINH', 'Nam Định'),
        ('NGHE_AN', 'Nghệ An'),
        ('NINH_BINH', 'Ninh Bình'),
        ('NINH_THUAN', 'Ninh Thuận'),
        ('PHU_THO', 'Phú Thọ'),
        ('PHU_YEN', 'Phú Yên'),
        ('QUANG_BINH', 'Quảng Bình'),
        ('QUANG_NAM', 'Quảng Nam'),
        ('QUANG_NGAI', 'Quảng Ngãi'),
        ('QUANG_NINH', 'Quảng Ninh'),
        ('QUANG_TRI', 'Quảng Trị'),
        ('SOC_TRANG', 'Sóc Trăng'),
        ('SON_LA', 'Sơn La'),
        ('TAY_NINH', 'Tây Ninh'),
        ('THAI_BINH', 'Thái Bình'),
        ('THAI_NGUYEN', 'Thái Nguyên'),
        ('THANH_HOA', 'Thanh Hóa'),
        ('THUA_THIEN_HUE', 'Thừa Thiên Huế'),
        ('TIEN_GIANG', 'Tiền Giang'),
        ('TP_HO_CHI_MINH', 'TP. Hồ Chí Minh'),
        ('TRA_VINH', 'Trà Vinh'),
        ('TUYEN_QUANG', 'Tuyên Quang'),
        ('VINH_LONG', 'Vĩnh Long'),
        ('VINH_PHUC', 'Vĩnh Phúc'),
        ('YEN_BAI', 'Yên Bái')
    ]

    depart = models.CharField(max_length=100, null=True, choices=VIETNAM_PROVINCES)
    dest = models.CharField(max_length=100, null=True, choices=VIETNAM_PROVINCES)
    description = RichTextField()

    def __str__(self):
        return self.depart + ' ' + self.dest


class TicketPrice(BaseModel):
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def __str__(self):
        return f"{self.price}"


# Chuyến xe
class Trip(BaseModel):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='tríps')
    pickup_location = models.CharField(max_length=100, null=True)  # Nơi đón
    dropoff_location = models.CharField(max_length=100, null=True)
    avatar = CloudinaryField('car', null=True)
    price = models.ForeignKey(TicketPrice, on_delete=models.SET_NULL, default=1, null=True)

    @property
    def seat_numbers(self):
        tickets = self.tickets.all()
        seat_numbers_list = [ticket.seat_number for ticket in tickets if ticket.seat_number]
        return seat_numbers_list

    def __str__(self):
        return f"Trip: {self.pickup_location} - {self.dropoff_location}, Price: {self.price}"


class Ticket(BaseModel):
    SEAT_CHOICES = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),

    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=20, choices=SEAT_CHOICES, null=True)

    # @property
    # def price(self):
    #     return self.trip.price

    def __str__(self):
        return f"{self.trip}, {self.seat_number}"


class TicketSeller(BaseModel):
    license_number = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.license_number}"


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ticket_info = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} "


class Feedback(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='feedbacks', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.CharField(max_length=255, null=False)
    rating = models.IntegerField(default=0)  # Đánh giá từ 0 đến 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trip} {self.user.username}"
