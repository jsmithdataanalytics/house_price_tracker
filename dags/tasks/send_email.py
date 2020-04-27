import smtplib
from datetime import timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import plotly.graph_objects as go
from airflow.hooks.base_hook import BaseHook
from pendulum import Pendulum
from plotly.subplots import make_subplots

from utils import db

email_connection = BaseHook.get_connection('sender_email')


def send_email(**kwargs):
    execution_date: Pendulum = kwargs['execution_date']

    if execution_date.weekday() == 6:
        table = analyse_prices(execution_date=execution_date)
        report_text = create_html_report(table=table)
        __send_email(execution_date=execution_date, report_text=report_text)


def create_html_report(table: pd.DataFrame) -> str:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=table.index, y=table.average_price, name='Average price'), secondary_y=False)
    fig.add_trace(go.Scatter(x=table.index, y=table.num_listings, name='Number of listings'), secondary_y=True)
    fig.update_yaxes(title_text="<b>Price (£)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Number of listings</b>", secondary_y=True)

    return report_template.format(figure_div=fig.to_html(full_html=False, include_plotlyjs='cdn'))


def __send_email(execution_date: Pendulum, report_text: str):
    subject = f'Weekly House Price Report - {execution_date.strftime("%d/%m/%Y")}'
    body = 'A new house price report is available!'
    report_filename = f'house-price-report-{execution_date.strftime("%d-%m-%Y")}.html'
    report_path = f'reports/{report_filename}'

    with open(report_path, 'w') as report_file:
        report_file.write(report_text)

    with open(report_path, 'rb') as report_file:
        report_blob = report_file.read()

    s = smtplib.SMTP(host=email_connection.host, port=email_connection.port)
    s.starttls()
    s.login(user=email_connection.login, password=email_connection.password)

    for recipient in email_connection.extra_dejson['recipients']:
        msg = MIMEMultipart()
        msg['From'] = email_connection.login
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        attachment = MIMEBase('text', 'html')
        attachment.set_payload(report_blob)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename= {report_filename}')
        msg.attach(attachment)

        s.send_message(msg)

    s.quit()


def analyse_prices(execution_date: Pendulum) -> pd.DataFrame:
    listings = pd.DataFrame(db.select_all('Listings'))
    listings.drop('id', axis=1, inplace=True)
    listings.set_index('listing_id', inplace=True)
    listings = listings.astype({'num_bedrooms': 'float64', 'listed_on': 'datetime64', 'last_reduced_on': 'datetime64'})
    listings['date'] = listings.last_reduced_on.combine_first(listings.listed_on)
    listings['year'] = listings.date.apply(lambda date: date.year)
    listings['week'] = listings.date.apply(lambda date: date.week)
    listings['week_commencing'] = listings.date.apply(lambda date: date - timedelta(days=date.weekday()))
    grouped = listings.groupby('week_commencing')
    prices_by_week = grouped.mean().join(grouped.count(), rsuffix='_count')
    prices_by_week = prices_by_week.loc[prices_by_week.index.year >= 2020]
    prices_by_week = prices_by_week.loc[prices_by_week.index.date <= execution_date.date()]
    prices_by_week = prices_by_week.loc[:][['listing_price', 'listing_price_count']]
    prices_by_week.rename({'listing_price': 'average_price'}, axis=1, inplace=True)
    prices_by_week.rename({'listing_price_count': 'num_listings'}, axis=1, inplace=True)

    return prices_by_week


report_template = """
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{{ margin:0 100; background:whitesmoke; }}</style>
    </head>
    <body>
        <h1>House Price Report</h1>
        <h2>Weekly average asking price and weekly number of listings for houses in the West Midlands</h2>
        <div height="550" width="1000">
            {figure_div}
        </div>
    </body>
</html>
"""
