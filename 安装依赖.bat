@echo off
chcp 65001 >nul
echo 正在安装依赖...
echo.

echo Step 1/3: 安装 playwright 包...
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

echo.
echo Step 2/3: 设置下载镜像...
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright

echo.
echo Step 3/3: 安装 chromium 浏览器（约100MB，请耐心等待）...
python -m playwright install chromium

echo.
echo ============================================
echo 安装完成！
echo ============================================
pause

