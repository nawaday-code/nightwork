import csv
import datetime

# Read calendar.csv file and store its contents in an array
calendar_data = []
is_first_row = True
with open('calendar.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not is_first_row and row:
            calendar_data.append(row)
        is_first_row = False   

        

# Prompt for start_date and end_date
print("カレンダー作成の開始日(YYYY/MM/DD)と終了日(YYYY/MM/DD)を入力してください。")
start_date = input("開始日を入力 (YYYY/MM/DD): ")
end_date = input("終了日を入力 (YYYY/MMDD): ")

# Convert input strings to date objects
try:
    start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d").date()

    if start_date >= end_date:
        print("エラー: 開始日よりも終了日が未来または同じ日付です。")
        exit()
except ValueError:
    print("入力された値が正しくありません。プログラムを終了します。")
    exit()

# Generate dates for Sundays, 2nd Saturdays, and 4th Saturdays between start_date and end_date
current_date = start_date
while current_date <= end_date:
    dates_to_generate = []
    if current_date.weekday() == 6:  # Sunday
        dates_to_generate.append(current_date.strftime("%Y/%m/%d"))
        dates_to_generate.append('日曜日')  # Sunday
    elif current_date.weekday() == 5:  # Saturday
        if (current_date.day // 7) == 1:  # 2nd Saturday
            dates_to_generate.append(current_date.strftime("%Y/%m/%d"))
            dates_to_generate.append('第2土曜日')
        if (current_date.day // 7) == 3:  # 4th Saturday
            dates_to_generate.append(current_date.strftime("%Y/%m/%d"))
            dates_to_generate.append('第4土曜日')
    if dates_to_generate:
        for data in calendar_data:
            if data[0] == current_date.strftime("%Y/%m/%d") and data[1] == '':
                calendar_data.append(dates_to_generate)
                break
       
    current_date += datetime.timedelta(days=1)


    calendar_data.sort(key=lambda x: datetime.datetime.strptime(x[0], "%Y/%m/%d").date())

    with open('tokai-calendar.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in calendar_data:
            writer.writerow(data)


