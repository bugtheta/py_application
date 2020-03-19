import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮件服务设置
mail_host = 'smtp.yourcompany.com'
mail_user = '****@yourcompany.com'  # 你的邮箱账号
mail_pass = '******'  # 你的邮箱密码

# 邮件内容编写
sender = '******@yourcompany.com'  # 发件人显示
receivers = ['******@yourcompany.com']  # 收集人显示
subject = '我是一个粉刷匠'  # 邮件主题
message = MIMEText('粉刷本领强', 'plain', 'utf-8')  # 邮件正文内容

# 将内容填入到message对象中
message['Subject'] = Header(subject)  # 邮件的title
message['From'] = Header(sender)  # 邮件显示的发件人
message['To'] = Header(''.join(receivers))  # 邮件显示的收件人

# try except来进行错误提醒
try:
    smtpObj = smtplib.SMTP()
    # 连接
    smtpObj.connect(mail_host, 25)
    # 登录
    smtpObj.login(mail_user, mail_pass)
    # 发送
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    # 退出
    smtpObj.quit()
    print('success!!!')
except smtplib.SMTPException as e:
    print('fail!!!', e)
