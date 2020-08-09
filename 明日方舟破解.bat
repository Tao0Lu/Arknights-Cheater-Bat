@echo off
set porxy=12450
if not exist %cd%\character_table.json (bitsadmin /transfer "下载character_table.json中(github被dns污染，如果不成功请检测hosts配置)" /download /priority normal "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json" %cd%\character_table.json)
if not exist %cd%\mitmdump.exe (echo.mitmdump.exe不存在&pause&exit)
for /f "tokens=4" %%a in ('route print^|findstr 0.0.0.0.*0.0.0.0') do ( set ip=%%a )
:main
echo.明日方舟破解 2020.8.9 update forked from GhostStar/Arknights-Armada
choice /m "是否增加自定义干员(Y是N否)"
if %errorlevel%==1 (goto customChar)
if %errorlevel%==2 (echo.noCustomChar>chatList.txt)
goto run
:customChar
cls
echo.自定义干员是在已拥有的干员之后增加自定义干员，但无法编入编队和使用(看用的)。
echo.自定义干员可在chatList.txt中编辑，为干员charId(可从character_table.json查询)，类似于这样：
echo.    char_285_medic2
echo.    char_286_cast3
echo.    char_376_therex
echo.    ......
choice /m "是否返回(Y是N否)"
if %errorlevel%==1 (goto main)
choice /m "是否生成一个全干员的chatList(Y是N否)"
if %errorlevel%==1 (
if exist %cd%\chatList.txt (del /f chatList.txt)
for /f "delims=" %%i in ('type "character_table.json"^|findstr "\<char.*\{" character_table.json') do (set "v=%%i"&setlocal enabledelayedexpansion&set "v=!v:~3!"&set "v=!v:~0,-4!"&echo !v!>>chatList.txt&endlocal)
)
if %errorlevel%==2 (
echo.请在chatList.txt中添加自定义角色
pause)
:run
echo.请在手机或模拟器中完成以下配置：
echo.1.确保手机或模拟器和电脑在同一局域网下。
echo.2.进入手机或模拟器WLAN(Wi-Fi)设置配置手机代理。
echo.    安卓：修改网络-高级选项-代理-手动
echo.    iOS：HTTP代理-配置代理-手动
echo.        服务器：%ip%
echo.        端口：%porxy%
echo.    保存/储存
echo.3.进入网站mitm.it下载证书(iOS为描述文件)并安装。
echo.4.重新进入游戏。
echo.
pause
echo.
echo.按下ctrl+c关闭破解
mitmdump.exe -s .\main.py --ssl-insecure -p %porxy%
