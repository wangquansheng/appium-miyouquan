import re
import time
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages.call.CallPage import CallPage

from pages.guide import GuidePage
from pages.login.LoginPage import OneKeyLoginPage
from pages.message.MessagePic import MessagePicPage
from pages.message.NewMessage import NewMessagePage
from pages.message.message import MessagePage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(object):
    """
    分解前置条件
    """

    @staticmethod
    def select_single_cmcc_android_4g_client():
        """
        启动
        1、4G，安卓客户端
        2、移动卡
        :return:
        """
        client = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        client.connect_mobile()

    @staticmethod
    def select_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return
        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()
        guide_page.click_start_the_one_key()

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        one_key.click_sure_login()
        # 等待消息页
        gp = GuidePage()
        try:
            gp.click_the_checkbox()
            gp.click_the_no_start_experience()
        except:
            pass
        cp = CallPage()
        cp.click_contact_tip()
        return login_number

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().capabilities['appPackage']
        current_mobile().terminate_app(app_id)

    @staticmethod
    def background_app(seconds):
        """后台运行"""
        current_mobile().background_app(seconds)

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.cmic.college'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def make_already_in_call_page():
        """
        前置条件：
        1.已登录客户端
        2.当前在通话页面
        """
        # 如果当前页面是在通话录页，不做任何操作
        call_page = CallPage()
        if call_page.is_on_this_page():
            return
        # 如果当前页面已经是一键登录页，进行一键登录页面
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            Preconditions.login_by_one_key_login()
            return
        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)
            # 跳过引导页
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_message_chart_page():
        """
        前置条件：
        1.已登录客户端
        2.当前在消息会话页面
        """
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        call_page = CallPage()
        mep = MessagePage()
        if mep.is_on_this_chart_page():
            return
        if mep.is_on_this_page():
            mep.click_add()
            mep.click_add_message()
            nmp = NewMessagePage()
            nmp.wait_for_page_new_message()
            nmp.click_contact_one()
            return
        if call_page.is_on_this_page():
            call_page.open_message_page()
            mep.click_add()
            mep.click_add_message()
            nmp = NewMessagePage()
            nmp.wait_for_page_new_message()
            nmp.click_contact_one()
            return
        # 进入一键登录页
        call_page.open_message_page()
        mep.click_add()
        mep.click_add_message()
        nmp = NewMessagePage()
        nmp.wait_for_page_new_message()
        nmp.click_contact_one()
        # Preconditions.make_already_in_call_page()
        # call = CallPage()
        # call.open_message_page()
        # mep = MessagePage()
        # mep.wait_for_page_message()
        # mep.click_add()
        # mep.click_add_message()
        # nmp = NewMessagePage()
        # nmp.wait_for_page_new_message()
        # nmp.click_contact_one()


class MessageTest(TestCase):
    """Message 模块"""

    # @staticmethod
    # def setUp_test_message_0001():
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     Preconditions.make_already_in_message_chart_page()
    #
    # @tags('ALL', 'SMOKE', 'CMCC')
    # def test_message_0001(self):
    #     """ 本网正常网络首次登录4G-登录响应"""
    #     mep = MessagePage()
    #     mep.wait_for_page_chart_message()
    #     # 1.长按“录制语音”icon,是否有取消按钮
    #     mep.click_record_audio()
    #     mep.long_click_record_audio()
    #     mep.is_exist_cancel_audio()
    #
    # @staticmethod
    # def setUp_test_message_0002():
    #     Preconditions.select_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     Preconditions.make_already_in_message_chart_page()
    #
    # @tags('ALL', 'SMOKE', 'CMCC')
    # def test_message_0002(self):
    #     """ 取消录制语音消息"""
    #     mep = MessagePage()
    #     mep.wait_for_page_chart_message()
    #     # 1.长按“录制语音”icon,是否有取消按钮
    #     mep.click_record_audio()
    #     mep.press_and_move_to_el("开始录音", "取消录音")

    @staticmethod
    def setUp_test_message_0003():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_message_0003(self):
        """ 发送语音消息"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.长按“录制语音”icon
        mep.click_record_audio()
        mep.long_click_record_audio()
        time.sleep(5)

    @staticmethod
    def setUp_test_message_0004():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_message_0004(self):
        """ 会话界面使用录音功能发送0秒语音"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击“录制语音”icon，检验有时间太短提示
        mep.click_record_audio()
        # mep.long_click_record_audio(time=100, wait_time=0.5)
        mep.click_start_record_audio()
        if not mep.is_toast_exist("时间太短"):
            raise AssertionError("没有此时间太短提示框")

    @staticmethod
    def setUp_test_message_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_message_0005(self):
        """ 消息会话-发送相册照片页面显示"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.校验a返回按钮，b照片，视频可勾选状态，c 发送按钮匹配
        menu = {"返回", "预览", "原图", "发送"}
        mpp.page_contain_ele(menu)
        mpp.is_select_pic()
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(\d+/9\)', flag))

    @staticmethod
    def setUp_test_message_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_message_0006(self):
        """ 消息会话-发送相册照片页面显示"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.a 未勾选时，预览显示置灰；
        self.assertEquals(mpp.is_click(), False)
        # b勾选图片，张数显示;
        mpp.select_pic(2)
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(2/9\)', flag))
        mpp.select_pic(2)
        mpp.select_pic(14)
        self.assertEquals(mpp.is_toast_exist("最多只能选择9张照片"), True)
        # c 最多可勾选9张图片

    @staticmethod
    def setUp_test_message_0007():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_chart_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_message_0007(self):
        """ 消息会话-发送相册照片-预览照片页面"""
        mep = MessagePage()
        mep.wait_for_page_chart_message()
        # 1.点击点击图片按钮
        mep.click_pic()
        mpp = MessagePicPage()
        mpp.wait_for_page_select_pic()
        # 2.a 未勾选时，预览显示置灰；
        self.assertEquals(mpp.is_click(), False)
        # b勾选图片，张数显示;
        mpp.select_pic(2)
        flag = mpp.get_pic_send_info()
        self.assertIsNotNone(re.match(r'发送\(2/9\)', flag))
        mpp.select_pic(2)
        # c 最多可勾选9张图片
        mpp.select_pic(14)
        self.assertEquals(mpp.is_toast_exist("最多只能选择9张照片"), True)
        # 3.点击预览照片
        mpp.click_pre_view()
        time.sleep(32)



