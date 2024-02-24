import os.path
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Phạm vi truy cập của ứng dụng (cần chỉnh sửa nếu cần thiết)
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate_google_calendar():
    creds = None
    # Kiểm tra xem đã tồn tại tệp token.json chứa thông tin xác thực chưa
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Nếu không có thông tin xác thực hoặc thông tin xác thực hết hạn
    if not creds or not creds.valid:
        # Nếu token hết hạn và có refresh token, tiến hành làm mới token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Nếu không có thông tin xác thực hoặc refresh token, thực hiện xác thực mới
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Lưu thông tin xác thực vào tệp token.json cho lần chạy tiếp theo
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def list_upcoming_holidays():
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
                holiday_dates.append((event_date.month, event_date.day))
                print(start, event["summary"])
        return holiday_dates
    except Exception as e:
        print(f"Lỗi khi truy vấn sự kiện từ Google Calendar API: {str(e)}")


if __name__ == "__main__":
    list_upcoming_holidays()
