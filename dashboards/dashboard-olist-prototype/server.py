import pandas as pd
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget
from shared import orders_df


def server (input, output, session): 

    # Create filtered copy of source data
    @reactive.calc
    def filtered_df():
        data = orders_df.copy()

        # Purchase date filter
        data = data[data['purchase_timestamp'].between(str(input.purchase_date()[0]), str(input.purchase_date()[1]))]
        # Delivery status filter
        data = data[data['status'].isin(input.status())]
        # Customer state filter
        data = data[data['customer_state_name'].isin(input.customer_state())]
        # Product category filter (modify to handle multipe selections)
        data = data[data['main_category'].isin(input.main_category())]
        # Payment type filter
        data = data[data['largest_single_payment_type'].isin(input.payment_type())]

        return data

    # (Overview) Value box calculations
    @render.text
    def total_orders():
        orders = len(filtered_df().order_id.unique())
        return orders

    @render.text
    def total_revenue():
        total_value = filtered_df().items_total_value.sum().round(2)
        # Apply assumed earnings percentage + shipping cost
        revenue = total_value * 0.23
        return f'${revenue}'

    @render.text
    def avg_order_value():
        total_value = filtered_df().items_total_value.sum()
        revenue = total_value * 0.23
        orders = len(filtered_df().order_id.unique())
        return f'${round(revenue / orders, 2)}'

    @render.text
    def avg_review_score():
        score = filtered_df().review_rating.mean()
        return round(score, 1)

    @render.text
    def late_delivery_rate():
        rate = filtered_df().is_late.mean()
        return f'{round(rate * 100, 1)}%'

    @render_widget
    def monthly_order_chart():

        # Aggregate orders by month
        data = filtered_df()
        monthly = (
            data.groupby('purchase_month', as_index = False)
                .agg(
                    orders = ('order_id', 'count'), 
                    revenue = ('items_total_value', 'sum')
                )
                .sort_values('purchase_month')
        )
        metric = input.trend_metric()
        label = 'Orders' if metric == 'orders' else 'Revenue (R$)'
        fig = px.line(monthly, x = 'purchase_month', y = metric, markers = True, labels = {metric: label, 'purchase_month': 'Purchase month'})
        if metric == 'revenue':
            fig.update_yaxes(tickprefix = 'R$ ', tickformat = ',.0f')
        else:
            fig.update_yaxes(tickformat = ',d')
        # fig.update_layout(margin = dict(l = 10, r = 10, t = 10, b = 10))
        return fig

    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    @render_widget
    def weekday_hour_heatmap():
        data = filtered_df()
        grid = (
            pd.crosstab(data['purchase_weekday'], data['purchase_hour'])
                .reindex(index = WEEKDAYS, columns = range(24), fill_value = 0)
        )
        fig = px.imshow(
            grid,
            labels=dict(x='Hour of day', y='', color='Orders'),
            color_continuous_scale='Blues',
            aspect='auto',
        )
        fig.update_xaxes(dtick = 1)
        fig.update_traces(hovertemplate = '%{y}, %{x}:00<br>Orders: %{z:,}<extra></extra>')
        fig.update_layout(margin = dict(l = 10, r = 10, t = 10, b = 10))
        return fig
