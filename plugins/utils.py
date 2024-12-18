# Placeholder

    def __init__(self, email: Optional[str] = None, pwdhash: Optional[str] = None, salt: Optional[str] = None):
        """User object

        Args:
            email (Optional[str], optional): User's email. Defaults to None.
            pwdhash (Optional[str], optional): Hashcode of the user's password. Defaults to None.
            salt (Optional[str], optional): Salt of the hashcode. Defaults to None.
        """
        self.email = email
        self.pwdhash = pwdhash
        self.salt = salt


class Group:


def _send_mail(dest: str, authcode: str):
    mail_html = f"""<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>您的验证码为：</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>
<p class=MsoNormal align=center style='margin-top:7.8pt;margin-right:0cm;
margin-bottom:7.8pt;margin-left:0cm;mso-para-margin-top:.5gd;mso-para-margin-right:
0cm;mso-para-margin-bottom:.5gd;mso-para-margin-left:0cm;text-align:center;
layout-grid-mode:char'><b><span lang=EN-US style='font-size:22.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-font-family:Arial;
letter-spacing:3.0pt'>{authcode}<o:p></o:p></span></b></p>
<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>此验证码包含数字与大写英文字母，输入时请注意字母大小写是否正确。验证码</span><span lang=EN-US
style='font-size:14.0pt;font-family:"Times New Roman",serif;mso-fareast-font-family:
宋体;mso-bidi-theme-font:minor-bidi'>10</span><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>分钟内有效。</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>"""
    message = MIMEText(mail_html, 'html', 'utf-8')
    message['From'] = 'Cloud Storage <jinyi.xia@foxmail.com>'
    message['To'] = f'<{dest}>'
    message['Subject'] = Header("验证码", 'utf-8')
    message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    retval = True
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com')
        server.login('jinyi.xia@foxmail.com', 'owkqtmqtphhpdhhi')
        server.sendmail('jinyi.xia@foxmail.com', dest, message.as_string())
        # server.login('vericode_sender@yeah.net', 'ROHFXNVSDLWBIKFA')
        # server.sendmail('vericode_sender@yeah.net', dest, message.as_string())
        server.quit()
    except:
        retval = False
    return retval



