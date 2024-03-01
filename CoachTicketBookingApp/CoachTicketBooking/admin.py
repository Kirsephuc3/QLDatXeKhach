from django.utils.safestring import mark_safe
from .models import User, TicketPrice, Route, Driver, Trip, Ticket, TicketSeller, Customer
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


# # Phạm vi truy cập của ứng dụng (cần chỉnh sửa nếu cần thiết)
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
#
#
# def authenticate_google_calendar():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     return creds
#
#
# def get_holidays():
#     try:
#         # Xác thực và tạo kết nối tới Google Calendar API
#         credentials = authenticate_google_calendar()
#         service = build("calendar", "v3", credentials=credentials)
#
#         # Lấy ngày hiện tại
#         now = datetime.datetime.utcnow()
#
#         # Tạo ngày bắt đầu là ngày hiện tại
#         start_date = now.isoformat() + 'Z'
#
#         # Gọi Google Calendar API để lấy sự kiện sắp tới
#         events_result = service.events().list(
#             calendarId="vi.vietnamese#holiday@group.v.calendar.google.com",
#             timeMin=start_date,
#             maxResults=1000,  # Số lượng sự kiện tối đa
#             singleEvents=True,
#             orderBy="startTime"
#         ).execute()
#
#         # Lấy danh sách sự kiện từ kết quả trả về
#         events = events_result.get("items", [])
#         holiday_dates = []
#
#         if not events:
#             print("Không có ngày lễ nào sắp tới trong năm.")
#         else:
#             print("Ngày lễ sắp tới trong năm:")
#             for event in events:
#                 start = event["start"].get("date")
#                 event_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
#                 holiday_dates.append(event_date)
#
#         return holiday_dates
#     except Exception as e:
#         print(f"Lỗi khi truy vấn sự kiện từ Google Calendar API: {str(e)}")
#         return []


# Đăng ký model User với custom admin
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'role']
    readonly_fields = ['image']

    def image(self, obj):
        return mark_safe(
            f"<img src='{obj.avatar.url}' width=150/>"
        )

    def save_model(self, request, obj, form, change):
        if obj.pk is not None:
            orig = User.objects.get(pk=obj.pk)
            if orig.password != obj.password:
                obj.password = make_password(obj.password)
        else:
            obj.password = make_password(obj.password)
        obj.save()


class TripAdmin(admin.ModelAdmin):
    list_display = ['route', 'start_time', 'end_time', 'driver', 'pickup_location', 'dropoff_location', 'price']
    readonly_fields = ['image']

    # def save_model(self, request, obj, form, change):
    #     holiday_dates = get_holidays()
    #     print(get_holidays())
    #     depart_date = obj.departure_date
    #
    #     if depart_date in holiday_dates:
    #         old_price = obj.price.price  # Lưu giá trị cũ
    #         obj.price.price *= Decimal('1.1')  # Tăng giá 10%
    #         new_price = obj.price.price  # Lấy giá trị mới
    #
    #         # Tạo một bản ghi mới cho giá trị cũ
    #         TicketPrice.objects.create(price=old_price)
    #
    #         # Cập nhật giá vé trong bảng TicketPrice
    #         ticket_price_instance = TicketPrice.objects.get(pk=obj.price.pk)
    #         ticket_price_instance.price = new_price
    #         ticket_price_instance.save()
    #
    #     super().save_model(request, obj, form, change)

    def image(self, obj):
        return mark_safe(
            f"<img src='{obj.avatar.url}' width=150/>"
        )


# CKEDITOR FORM
class RouteForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Route
        fields = '__all__'


class RouteAdmin(admin.ModelAdmin):
    list_display = ['depart', 'dest']
    form = RouteForm


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['ticket_info', 'user']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['trip', 'seat_number']


# Đăng ký các model với custom admin
admin.site.register(TicketPrice)
admin.site.register(Route, RouteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Driver)
admin.site.register(Trip, TripAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketSeller)
admin.site.register(Customer, CustomerAdmin)
