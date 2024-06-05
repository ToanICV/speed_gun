#include <QCoreApplication>
#include <QTimer>

int demo(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    // Tạo timer với khoảng thời gian 1 giây
    QTimer timer;
    timer.setInterval(1000);

    // Kết nối tín hiệu timeout với slot xử lý sự kiện
    QObject::connect(&timer, &QTimer::timeout, []() {
        // Xử lý sự kiện khi timer hết giờ
        printf("Event 1 sec trigger...\n");
    });

    // Bắt đầu timer
    timer.start();

    // Tạo một QEventLoop để chờ sự kiện
    QEventLoop loop;
    loop.exec(); // Chạy vòng lặp sự kiện cho đến khi gặp sự kiện thoát

    return 0;
}
