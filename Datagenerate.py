import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

# Define the date range for a whole year
start_date = datetime(2019, 1, 1)
end_date = datetime(2022, 12, 31)

# Get the trading calendar for India's NSE Nifty index
nse = mcal.get_calendar('NSE')
trading_days = nse.valid_days(start_date=start_date, end_date=end_date)

# Define the trading hours in IST
trading_start_time = datetime.strptime('09:15:00', '%H:%M:%S').time()
trading_end_time = datetime.strptime('15:10:00', '%H:%M:%S').time()

# Define the number of trades you want to generate
num_trades = len(trading_days)  # One trade per trading day

# Create empty lists to store trading data
trade_ids = []
dates = []
days_of_week = []  # Added Day column
entry_times = []
exit_times = []
ticker_symbols = []
long_short = []
entry_prices = []
exit_prices = []
num_shares = []
stop_loss_prices = []
take_profit_prices = []
commission_paid = []
trade_durations = []  # Modified to calculate trade duration
profit_loss = []  # Added column for profit/loss
trade_outcomes = []
strategies_used = []
notes = []

# Generate random trading data
for i in range(num_trades):
    trade_date = trading_days[i]
    day_of_week = trade_date.strftime('%A')  # Get the day of the week
    
    # Ensure the trade day is Monday to Friday
    if day_of_week not in ['Saturday', 'Sunday']:
        trade_ids.append(random.randint(1000, 9999))
        dates.append(trade_date.date())  # Removing the time from the date
        days_of_week.append(day_of_week)
    
        long_or_short = random.choice(['Long', 'Short'])
        long_short.append(long_or_short)
    
        # Calculate trading duration in seconds
        trading_duration_seconds = (trading_end_time.hour * 3600 + trading_end_time.minute * 60) - (trading_start_time.hour * 3600 + trading_start_time.minute * 60)
    
        # Generate random entry and exit times within trading hours
        if trading_duration_seconds >= 60:  # Ensure at least 1 minute of trading time
            entry_time_seconds = random.randint(0, trading_duration_seconds)
            exit_time_seconds = entry_time_seconds + random.randint(1, trading_duration_seconds - entry_time_seconds)
    
            entry_time = (datetime.combine(trade_date, trading_start_time) + timedelta(seconds=entry_time_seconds)).time()
            exit_time = (datetime.combine(trade_date, trading_start_time) + timedelta(seconds=exit_time_seconds)).time()
        else:
            # Set entry and exit times to the start of trading hours if not enough time
            entry_time = trading_start_time
            exit_time = trading_start_time
        
        entry_times.append(entry_time)
        exit_times.append(exit_time)
        
        # Calculate the trade duration
        entry_datetime = datetime.combine(trade_date, entry_time)
        exit_datetime = datetime.combine(trade_date, exit_time)
        duration = exit_datetime - entry_datetime
        trade_durations.append(duration.total_seconds() / 60)  # Convert to minutes
        
        # Generate random entry and exit prices
        entry_price = round(random.uniform(100, 300), 2)
        exit_price = round(random.uniform(100, 300), 2)
        entry_prices.append(entry_price)
        exit_prices.append(exit_price)
        
        # Calculate profit/loss based on long or short trade
        if long_or_short == 'Long':
            pl = (exit_price - entry_price)  # Profit if positive, Loss if negative
        else:
            pl = (entry_price - exit_price)  # Profit if positive, Loss if negative
        profit_loss.append(pl)
        
        # Determine the trade outcome
        if pl >= 0:
            trade_outcome = 'Win'
        else:
            trade_outcome = 'Loss'
        trade_outcomes.append(trade_outcome)
        
        # Replace stock symbols related to India stocks with Nifty index options
        ticker_symbols.append(random.choice(['BANKNIFTY', 'NIFTY']))
        
        num_shares.append(random.randint(1, 1000))
        stop_loss_prices.append(round(random.uniform(80, 150), 2))
        take_profit_prices.append(round(random.uniform(300, 400), 2))
        commission_paid.append(round(random.uniform(1, 10), 2))
        
        strategies_used.append(random.choice(['SMC', 'BREAKOUT', 'ALGO']))
        notes.append("Randomly generated trade")

# Create a DataFrame
data = {
    'Trade ID': trade_ids,
    'Date': dates,
    'Day': days_of_week,  # Add Day column
    'Entry Time': entry_times,
    'Exit Time': exit_times,
    'Ticker Symbol': ticker_symbols,
    'Long/Short': long_short,
    'Entry Price': entry_prices,
    'Exit Price': exit_prices,
    'Number of Shares/Contracts': num_shares,
    'Stop-Loss Price': stop_loss_prices,
    'Take-Profit Price': take_profit_prices,
    'Commission Paid': commission_paid,
    'Trade Duration (minutes)': trade_durations,
    'Profit/Loss': profit_loss,
    'Trade Outcome': trade_outcomes,
    'Strategy Used': strategies_used,
    'Notes': notes
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('random_trading_data.csv', index=False)