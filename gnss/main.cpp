#include <QCoreApplication>
#include <QTimer>
#include <QtSerialPort/QSerialPort>
#include <QtSerialPort/QSerialPortInfo>
#include <QDebug>
#include <QByteArray>
#include "utils.h"

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    // Tìm serial port (COM port)
    QList<QSerialPortInfo> availablePorts = QSerialPortInfo::availablePorts();
    QSerialPortInfo info; // Khai báo biến info
    for (const QSerialPortInfo& port : availablePorts) {
        printf("Port name: %s\n", port.portName().toUtf8().constData());
        // Thay thế "COM3" bằng tên COM port phù hợp
        if (port.portName() == "COM3") {
            info = port;
            break; // Thoát vòng lặp khi tìm thấy
        }
    }
    if (!info.isValid()) {
        qDebug() << "Không tìm thấy serial port COM3";
        return 1;
    }

    // Khởi tạo serial port
    QSerialPort serialPort;
    serialPort.setPort(info);
    serialPort.setBaudRate(QSerialPort::Baud115200);
    serialPort.setDataBits(QSerialPort::Data8);
    serialPort.setParity(QSerialPort::NoParity);
    serialPort.setStopBits(QSerialPort::OneStop);
    serialPort.setFlowControl(QSerialPort::NoFlowControl);

    // Mở kết nối serial port
    if (!serialPort.open(QIODevice::ReadWrite)) {
        qDebug() << "Không thể mở serial port";
        return 1;
    }

    // Gửi lệnh AT
    QByteArray command1 = "AT+CGPSNMEAPORTCFG=3\r\n";
    QByteArray command2 = "AT+CGPSINFOCFG=1,31\r\n";
    serialPort.write(command1);
    serialPort.write(command2);

    // Tạo timer để đọc dữ liệu sau 1 giây
    QTimer timer;
    timer.setInterval(1000);
    QObject::connect(&timer, &QTimer::timeout, [&serialPort]() {
        // Đọc dữ liệu từ serial port
        QByteArray data = serialPort.readAll();
        if (!data.isEmpty()) {
            string nmea_data = data.toStdString();
            cout << "Recv: " << nmea_data;
            vector<string> lines = split(nmea_data, '\n');
            for (const string& line : lines){
                vector<string> parts = split(line, ',');
                if (parts[0] == "$GPRMC"){
                    if (parts[2] == "A"){   // prefix
                        cout << "lat: " << ((int)stof(parts[3])/100)  + (((long)(stof(parts[3])*100000)%10000000)/100000.0)/60.0 << endl;
                        cout << "lng: " << ((int)stof(parts[5])/100)  + (((long)(stof(parts[5])*100000)%10000000)/100000.0)/60.0 << endl;
                    }
                    else{
                        ;
                    }
                }
                else{
                    ;
                }
            }
        }
        else{
            string gprmc_sentence = "$GPGGA,071835.170,2104.177,N,10546.631,E,1,12,1.0,0.0,M,0.0,M,,*64\n\
$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30\n\
$GPRMC,071835.170,A,2104.177,N,10546.631,E,038.9,167.6,230324,000.0,W*70";
            vector<string> lines = split(gprmc_sentence, '\n');
            for (const string& line : lines){
                vector<string> parts = split(line, ',');
                if (parts[0] == "$GPRMC"){
                    if (parts[2] == "A"){   // prefix
                        cout << "lat: " << ((int)stof(parts[3])/100)  + (((long)(stof(parts[3])*100000)%10000000)/100000.0)/60.0 << endl;
                        cout << "lng: " << ((int)stof(parts[5])/100)  + (((long)(stof(parts[5])*100000)%10000000)/100000.0)/60.0 << endl;
                    }
                    else{
                        ;
                    }
                }
                else{
                    ;
                }
            }
        }
    });
    timer.start();

    return app.exec();
}
