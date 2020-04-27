import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timedelta
import pandas as pd
from airflow.hooks.base_hook import BaseHook

from utils import db

email_connection = BaseHook.get_connection('sender_email')


def send_email(**kwargs):
    execution_date = kwargs['execution_date']
    table = analyse_prices()

    if execution_date.weekday() == 6:
        __send_email(subject=f'Weekly House Price Report - {execution_date.strftime("%d/%m/%Y")}', body=str(table))


def __send_email(subject: str, body: str):
    s = smtplib.SMTP(host=email_connection.host, port=email_connection.port)
    s.starttls()
    s.login(user=email_connection.login, password=email_connection.password)

    for recipient in email_connection.extra_dejson['recipients']:
        msg = MIMEMultipart()
        msg['From'] = email_connection.login
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        s.send_message(msg)

    s.quit()


def analyse_prices():
    listings = pd.DataFrame(db.select_all('Listings'))
    listings.drop('id', axis=1, inplace=True)
    listings.set_index('listing_id', inplace=True)
    listings = listings.astype({'num_bedrooms': 'float64', 'listed_on': 'datetime64', 'last_reduced_on': 'datetime64'})
    listings['date'] = listings.last_reduced_on.combine_first(listings.listed_on)
    listings['year'] = listings.date.apply(lambda d: d.year)
    listings['week'] = listings.date.apply(lambda d: d.week)
    listings['week_commencing'] = listings.date.apply(lambda d: d - timedelta(days=d.weekday()))
    grouped = listings.groupby('week_commencing')
    prices_by_week = grouped.mean().join(grouped.count(), rsuffix='_count')
    prices_by_week_2020 = prices_by_week.loc[prices_by_week.index.year == 2020]
    prices_by_week_2020 = prices_by_week_2020.loc[:][['listing_price', 'listing_price_count']]
    prices_by_week_2020.rename({'listing_price_count': 'count'}, axis=1, inplace=True)

    return prices_by_week_2020
