import easygui

url = easygui.enterbox()

import test_gevent
html = test_gevent.get_data(url)

#easygui.msgbox(html)
