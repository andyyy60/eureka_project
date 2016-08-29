import smtplib, argparse, urllib2, time, sys

def main():
    parser = argparse.ArgumentParser(description='Email healthcheck script')
    parser.add_argument('password', action='store', type=str, help='password')
    args = parser.parse_args()
    password = args.password


    while True:
        stat = True
        try:
            health = eval(urllib2.urlopen("http://localhost:5000/healthcheck").read())
        except:
            stat = False
        if stat == False or health['status'] != 'success':
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("klolwtfxd@gmail.com", password)

            msg = "Healthcheck failed, check Flask service"
            server.sendmail("klolwtfxd@gmail.com", "andyyy60@gmail.com", msg)
            server.quit()
            sys.exit(1)
        time.sleep(1800) #30 mins


######################################
if __name__ == "__main__":
    main()
######################################