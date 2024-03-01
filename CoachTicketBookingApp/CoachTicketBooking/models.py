import os
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from google.oauth2.credentials import Credentials
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.db import models
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime


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
        ('An Giang', 'An Giang'),
        ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
        ('Bạc Liêu', 'Bạc Liêu'),
        ('Bắc Giang', 'Bắc Giang'),
        ('Bắc Kạn', 'Bắc Kạn'),
        ('Bắc Ninh', 'Bắc Ninh'),
        ('Bến Tre', 'Bến Tre'),
        ('Bình Dương', 'Bình Dương'),
        ('Bình Định', 'Bình Định'),
        ('Bình Phước', 'Bình Phước'),
        ('Bình Thuận', 'Bình Thuận'),
        ('Cà Mau', 'Cà Mau'),
        ('Cao Bằng', 'Cao Bằng'),
        ('Cần Thơ', 'Cần Thơ'),
        ('Đà Nẵng', 'Đà Nẵng'),
        ('Đắk Lắk', 'Đắk Lắk'),
        ('Đắk Nông', 'Đắk Nông'),
        ('Điện Biên', 'Điện Biên'),
        ('Đồng Nai', 'Đồng Nai'),
        ('Đồng Tháp', 'Đồng Tháp'),
        ('Gia Lai', 'Gia Lai'),
        ('Hà Giang', 'Hà Giang'),
        ('Hà Nam', 'Hà Nam'),
        ('Hà Nội', 'Hà Nội'),
        ('Hà Tĩnh', 'Hà Tĩnh'),
        ('Hải Dương', 'Hải Dương'),
        ('Hải Phòng', 'Hải Phòng'),
        ('Hậu Giang', 'Hậu Giang'),
        ('Hòa Bình', 'Hòa Bình'),
        ('Hưng Yên', 'Hưng Yên'),
        ('Khánh Hòa', 'Khánh Hòa'),
        ('Kiên Giang', 'Kiên Giang'),
        ('Kon Tum', 'Kon Tum'),
        ('Lai Châu', 'Lai Châu'),
        ('Lạng Sơn', 'Lạng Sơn'),
        ('Lào Cai', 'Lào Cai'),
        ('Lâm Đồng', 'Lâm Đồng'),
        ('Long An', 'Long An'),
        ('Nam Định', 'Nam Định'),
        ('Nghệ An', 'Nghệ An'),
        ('Ninh Bình', 'Ninh Bình'),
        ('Ninh Thuận', 'Ninh Thuận'),
        ('Phú Thọ', 'Phú Thọ'),
        ('Phú Yên', 'Phú Yên'),
        ('Quảng Bình', 'Quảng Bình'),
        ('Quảng Nam', 'Quảng Nam'),
        ('Quảng Ngãi', 'Quảng Ngãi'),
        ('Quảng Ninh', 'Quảng Ninh'),
        ('Quảng Trị', 'Quảng Trị'),
        ('Sóc Trăng', 'Sóc Trăng'),
        ('Sơn La', 'Sơn La'),
        ('Tây Ninh', 'Tây Ninh'),
        ('Thái Bình', 'Thái Bình'),
        ('Thái Nguyên', 'Thái Nguyên'),
        ('Thanh Hóa', 'Thanh Hóa'),
        ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
        ('Tiền Giang', 'Tiền Giang'),
        ('TP. Hồ Chí Minh', 'TP. Hồ Chí Minh'),
        ('Trà Vinh', 'Trà Vinh'),
        ('Tuyên Quang', 'Tuyên Quang'),
        ('Vĩnh Long', 'Vĩnh Long'),
        ('Vĩnh Phúc', 'Vĩnh Phúc'),
        ('Yên Bái', 'Yên Bái')
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
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='trips')
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


@receiver(pre_save, sender=Trip)
def update_price_on_holiday(sender, instance, **kwargs):
    holiday_dates = get_holidays()
    depart_date = instance.departure_date

    if depart_date in holiday_dates:
        old_price = instance.price.price  # Lưu giá trị cũ
        instance.price.price *= Decimal('1.1')  # Tăng giá 10%
        new_price = instance.price.price  # Lấy giá trị mới

        # Tạo một bản ghi mới cho giá trị cũ
        TicketPrice.objects.create(price=old_price)

        # Cập nhật giá vé trong bảng TicketPrice
        ticket_price_instance = TicketPrice.objects.get(pk=instance.price.pk)
        ticket_price_instance.price = new_price
        ticket_price_instance.save()


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
    status = models.BooleanField(default=False)

    # @property
    # def price(self):
    #     return self.trip.price

    def __str__(self):
        return f"{self.trip}, {self.seat_number}"


class TicketSeller(BaseModel):
    license_number = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.license_number}"


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ticket_info = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} "


class Feedback(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='feedbacks', null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=255, null=False)
    rating = models.IntegerField(default=0)  # Đánh giá từ 0 đến 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.customer:
            return f"{self.trip} {self.customer.user.username}"
        else:
            return f"{self.trip} - No customer"


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate_google_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Lưu thông tin xác thực vào tệp token.json cho lần chạy tiếp theo
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_holidays():
    try:
        # Xác thực và tạo kết nối tới Google Calendar API
        credentials = authenticate_google_calendar()
        service = build("calendar", "v3", credentials=credentials)

        # Lấy ngày hiện tại
        now = datetime.datetime.utcnow()

        # Tạo ngày bắt đầu là ngày hiện tại
        start_date = now.isoformat() + 'Z'

        # Gọi Google Calendar API để lấy sự kiện sắp tới
        events_result = service.events().list(
            calendarId="vi.vietnamese#holiday@group.v.calendar.google.com",
            timeMin=start_date,
            maxResults=1000,  # Số lượng sự kiện tối đa
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        # Lấy danh sách sự kiện từ kết quả trả về
        events = events_result.get("items", [])
        holiday_dates = []

        if not events:
            print("Không có ngày lễ nào sắp tới trong năm.")
        else:
            print("Ngày lễ sắp tới trong năm:")
            for event in events:
                start = event["start"].get("date")
                event_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
                holiday_dates.append(event_date)

        return holiday_dates
    except Exception as e:
        print(f"Lỗi khi truy vấn sự kiện từ Google Calendar API: {str(e)}")
        return []
