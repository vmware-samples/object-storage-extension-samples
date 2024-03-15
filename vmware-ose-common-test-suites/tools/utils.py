import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from framework.libs.common.utils import read_yml


def get_and_update_mail_content(file, file_remote_path):
    with open(file, 'r+') as f:
        mail_body = f.read()

        f_n = file.split('/')[-1]

        insert_string1 = '<br/><p class="attribute"><strong>Report Link: </strong><a href="' \
                         + file_remote_path + '"> Report Link</a></p>'

        index_1 = mail_body.find("</h1>")
        index_2 = mail_body.find("Start Time:")
        new_mail_body = mail_body[:index_1 + 5] + insert_string1 + \
                        mail_body[index_2 - 30:]

        return new_mail_body


def upload_report(file_path, file_n, configs):
    usr = configs['artifacts_env']['usr']
    pwd = configs['artifacts_env']['password']
    url = configs['artifacts_env']['logs_link']

    if os.path.exists(file_path):
        res = os.popen('curl -u %s:%s -T %s %s; wait' % (usr, pwd, file_path, url)).readlines()
        print(res)
        print('Report Link: %s' % (url + file_n))
        return url + file_n

    return None


def send_email(file_n, local_folder, ose_profile_configs=None):
    if not ose_profile_configs:
        config_file_path = '/Users/elvisy/PycharmProjects/s3-test/prj/user_profile.yml'
        ose_profile_configs = read_yml(config_file_path)

    file_local_path = local_folder + "/report/" + file_n

    file_remote_path = upload_report(file_path=file_local_path, file_n=file_n, configs=ose_profile_configs.get('upload_config'))

    new_mail_body = get_and_update_mail_content(file_local_path, file_remote_path)

    msg = MIMEText(new_mail_body, 'html', 'utf-8')

    configs = ose_profile_configs.get('email_config')

    mailsubject = configs.get('subject')
    msg['Subject'] = Header(mailsubject, 'utf-8')

    sender = configs.get("sender")
    msg['From'] = sender

    if 'email_receivers' in ose_profile_configs:
        to_list = ose_profile_configs.get('email_receivers').split(' ')
    else:
        to_list = configs.get('receivers')

    msg['To'] = '; '.join(to_list)

    smtp_server = configs.get('email_server')
    server = smtplib.SMTP(smtp_server)
    server.sendmail(sender, to_list, msg.as_string())
    server.quit()

    return True


if __name__ == '__main__':
    pass
