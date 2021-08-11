from pyppeteer import launch
import asyncio
import time
# import schedule
import requests


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1920, "height": 1080})
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59")
    await page.goto('https://www.cdc.com.sg:8080/NewPortal/Booking/BookingPL.aspx', {"waitUntil": "networkidle0"})

    await page.setCookie({"name": "ASP.NET_SessionId", "value": "2etwaznhdz0fg3etis0mvq55"})

    await page.goto('https://www.cdc.com.sg:8080/NewPortal/Booking/BookingPL.aspx', {"waitUntil": "networkidle0"})

    dropdown = await page.xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlCourse"]')
    await dropdown[0].click()
    await page.keyboard.press("Space")
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")

    await page.waitForXPath('//*[@id="ctl00_ContentPlaceHolder1_ddlOthTeamID"]')
    time.sleep(5)
    await page.screenshot({'path': 'test1.png'})

    num_of_sessions = await page.querySelector("#ctl00_ContentPlaceHolder1_lblSessionNo")
    practical = await page.evaluate('(num_of_sessions) => num_of_sessions.textContent', num_of_sessions)
    date_of_session = await page.querySelector("#ctl00_ContentPlaceHolder1_lblFrom")
    date = await page.evaluate('(date_of_session) => date_of_session.textContent', date_of_session)
    print(practical)
    print(date)
    aug_slots = await page.querySelector('#ctl00_ContentPlaceHolder1_lblM2SesNo')
    aug = await page.evaluate('(aug_slots) => aug_slots.textContent', aug_slots)
    print(aug + " slots in Aug")

    if practical != '0':
        print("Slots available! With " + aug + " slots in Aug!")
        telegram_bot_sendtext(practical + " Slots available from " + date + " with " + aug + " slots in Aug!")
    else:
        print("No slots from team 3:(")
        other_teams = await page.querySelector('#ctl00_ContentPlaceHolder1_ddlOthTeamID > option:nth-child(2)')
        if other_teams is not None:
            print("Other teams exist")
            # if i want to confirm that there is more than 1 option in 2nd dropdown menu
            # other_team_num = await page.evaluate('(other_teams) => other_teams.textContent', other_teams)
            # print(other_team_num)
            telegram_bot_sendtext("No slots from team 3 but slots in other teams available!")
        else:
            print("No other teams")
            telegram_bot_sendtext("No slots available:(")

def telegram_bot_sendtext(bot_message):
    bot_token = '1613857380:AAFFb3BPriDUROzvx2bi8s8FdIgWpyEFbvY'
    bot_chatID = '238412962'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


# schedule.every(1).minutes.do(main)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

asyncio.get_event_loop().run_until_complete(main())
# asyncio.get_event_loop().run_forever()


# <span id="ctl00_ContentPlaceHolder1_lblSessionNo" style="font-size:12px;font-weight:bold;">0</span>

# //*[@id="ctl00_ContentPlaceHolder1_ddlOthTeamID"]/option[0]
# //*[@id="ctl00_ContentPlaceHolder1_ddlOthTeamID"]/option[1] = wait for
# //*[@id="ctl00_ContentPlaceHolder1_ddlOthTeamID"]/option[2]
# //*[@id="ctl00_ContentPlaceHolder1_ddlOthTeamID"]/option[1]
