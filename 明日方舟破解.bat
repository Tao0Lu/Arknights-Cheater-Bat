@echo off
set porxy=12450
if not exist %cd%\character_table.json (bitsadmin /transfer "����character_table.json��(github��dns��Ⱦ��������ɹ�����hosts����)" /download /priority normal "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json" %cd%\character_table.json)
if not exist %cd%\mitmdump.exe (echo.mitmdump.exe������&pause&exit)
for /f "tokens=4" %%a in ('route print^|findstr 0.0.0.0.*0.0.0.0') do ( set ip=%%a )
:main
echo.���շ����ƽ� 2020.8.9 update forked from GhostStar/Arknights-Armada
choice /m "�Ƿ������Զ����Ա(Y��N��)"
if %errorlevel%==1 (goto customChar)
if %errorlevel%==2 (echo.noCustomChar>chatList.txt)
goto run
:customChar
cls
echo.�Զ����Ա������ӵ�еĸ�Ա֮�������Զ����Ա�����޷������Ӻ�ʹ��(���õ�)��
echo.�Զ����Ա����chatList.txt�б༭��Ϊ��ԱcharId(�ɴ�character_table.json��ѯ)��������������
echo.    char_285_medic2
echo.    char_286_cast3
echo.    char_376_therex
echo.    ......
choice /m "�Ƿ񷵻�(Y��N��)"
if %errorlevel%==1 (goto main)
choice /m "�Ƿ�����һ��ȫ��Ա��chatList(Y��N��)"
if %errorlevel%==1 (
if exist %cd%\chatList.txt (del /f chatList.txt)
for /f "delims=" %%i in ('type "character_table.json"^|findstr "\<char.*\{" character_table.json') do (set "v=%%i"&setlocal enabledelayedexpansion&set "v=!v:~3!"&set "v=!v:~0,-4!"&echo !v!>>chatList.txt&endlocal)
)
if %errorlevel%==2 (
echo.����chatList.txt������Զ����ɫ
pause)
:run
echo.�����ֻ���ģ����������������ã�
echo.1.ȷ���ֻ���ģ�����͵�����ͬһ�������¡�
echo.2.�����ֻ���ģ����WLAN(Wi-Fi)���������ֻ�����
echo.    ��׿���޸�����-�߼�ѡ��-����-�ֶ�
echo.    iOS��HTTP����-���ô���-�ֶ�
echo.        ��������%ip%
echo.        �˿ڣ�%porxy%
echo.    ����/����
echo.3.������վmitm.it����֤��(iOSΪ�����ļ�)����װ��
echo.4.���½�����Ϸ��
echo.
pause
echo.
echo.����ctrl+c�ر��ƽ�
mitmdump.exe -s .\main.py --ssl-insecure -p %porxy%
