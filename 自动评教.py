from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs
import time,re

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def handle_dialog(dialog):
            print(f"检测到弹窗: {dialog.message}")
            dialog.accept()
            print("已自动确认弹窗")

        context.on("dialog", handle_dialog)

        try:
            print("正在访问教务系统...")
            page.goto("https://inquiry.ecust.edu.cn/jsxsd/")
            print("请在浏览器中完成登录...")

            page.wait_for_url("**/framework/xsMain.jsp", timeout=0)
            print("检测到登录成功，正在跳转...")
            print("正在等待页面元素加载...")

            block3_element = page.locator("div.wap a div.block3").first
            block3_element.wait_for(state="visible", timeout=30000)
            print("找到学生评教入口，正在点击...")
            block3_element.click()
            print("点击成功！等待页面加载...")

            page.wait_for_load_state("domcontentloaded", timeout=30000)
            print("页面加载完成")

            print("正在查找进入评价入口...")
            evaluate_link = page.locator('a[title="点击进入评价"]').first
            evaluate_link.wait_for(state="visible", timeout=30000)
            print("找到入口，正在点击...")
            evaluate_link.click()
            print("进入评价信息页面成功！")

            page.wait_for_load_state("domcontentloaded", timeout=30000)
            print("评价课程列表页面加载完成")

            print("正在查找所有评价课程...")
            pingjia_links = page.locator('a:text-is("评价")')
            total_courses = pingjia_links.count()
            print(f"共找到 {total_courses} 门课程待评教")

            for course_index in range(total_courses):
                print(f"\n{'='*50}")
                print(f'=== 开始评教第 {course_index + 1}/{total_courses} 门课程 ===')
                print(f"{'='*50}")

                new_page = context.new_page()
                pingjia_link = pingjia_links.nth(course_index)
                pingjia_link.wait_for(state="visible", timeout=30000)

                href = pingjia_link.get_attribute("href")
                print(f"获取到评价链接: {href}")

                match = re.search(r"openWindow\(['\"](.*?)['\"]", href)
                if match:
                    target_relative_url = match.group(1)
                    parsed = urlparse(target_relative_url)
                    params = parse_qs(parsed.query)

                    base_url = "https://inquiry.ecust.edu.cn" + parsed.path.split('/jsxsd')[0] + "/jsxsd" + parsed.path.replace('/jsxsd', '')
                    new_url = base_url
                    if params:
                        query_string = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                        new_url = f"{base_url}?{query_string}"

                print(f"解析后的链接: {new_url}")

                new_page.goto(new_url)
                print("正在加载评教页面...")

                new_page.wait_for_load_state("domcontentloaded", timeout=30000)
                print("评教页面加载完成")

                radio_buttons = new_page.locator('xpath=//input[@type="radio"][following-sibling::text()[normalize-space(.)="10"]]')
                count = radio_buttons.count()
                print(f"找到 {count} 个评价选项")

                for i in range(count):
                    radio_buttons.nth(i).click()
                    print(f"  已点击第 {i+1} 个选项")
                    new_page.wait_for_timeout(100)

                print("所有选项已点击，正在提交...")
                submit_button = new_page.locator('input#tj')
                submit_button.wait_for(state="visible", timeout=30000)
                submit_button.click()
                print(f"✓ 第 {course_index + 1} 门课程评教提交成功！")

                new_page.wait_for_timeout(1500)
                new_page.close()


            print(f"\n{'='*50}")
            print('所有课程评教完成！')
            print(f"{'='*50}")

            print("操作完成")
            time.sleep(5)

        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
