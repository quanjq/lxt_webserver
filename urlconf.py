# -*- coding:utf-8 -*-
import view

urlConf = [
    ("/update-action/", view.update_action),#修改返回pjs的报文,这个位置不要动
    ("/reset-password/index",view.index_of_reset_password),
    ("/open-acct/index", view.index_of_open_acct),#开户
    ("/change-bank-card/index", view.index_of_change_bank_card),#更换银行卡
    ("/stock-customer/index", view.index_of_stock_customer),#已迁移未开通
    ("/unbind/index", view.index_of_unbind),#解绑银行卡
    ("/payment-confirm/index", view.index_of_payment_confirm),#缴费申请
    ("/business-authorize-confirm/index", view.index_of_business_authorize_confirm),#投资免密y y
    ("/bespeak-investment-freeze-confirm/index", view.index_of_bespeak_investment_freeze_confirm),#预约投资y y
    ("/investment-freeze-confirm/index", view.index_of_investment_freeze_confirm),#投资y
    ("/withdrawals-confirm/index", view.index_of_withdrawals_confirm),#提现y
    ("/recharge-confirm/index", view.index_of_recharge_confirm),#充值
    ("/pay-confirm/index", view.index_of_pay_confirm),#定向支授权
    ("/unsubscribe/index", view.index_of_unsubscribe),#销户
    # ("/index/", view.index),#
]