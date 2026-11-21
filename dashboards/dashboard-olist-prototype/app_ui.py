import faicons as fa
from shiny import ui
from pathlib import Path
from htmltools import head_content
from shared import orders_df
from shinywidgets import output_widget
import datetime

# CSS file path
css_path = Path(__file__).parent / 'style.css'

# Filters
min_purchase_date = orders_df.purchase_timestamp.min()
max_purchase_date = orders_df.purchase_timestamp.max()

status = orders_df.status.unique().tolist()
customer_state = orders_df.customer_state_name.unique().tolist()
main_category = orders_df.main_category.unique().tolist() # Reduce dymanically based on other filter options
payment_type = orders_df.largest_single_payment_type.unique().tolist()

# Define the UI layout
app_ui = ui.page_navbar(
        ui.head_content(ui.include_css(css_path)),
        ui.nav_panel('Overview', 
            # ui.panel_title('In-Progress Demo Dashboard'),
            ui.div(
                {'class' : 'kpi-row'},
                ui.layout_columns(
                    # Value box statistics
                    ui.value_box(
                        'Orders:', ui.output_ui('total_orders'), showcase = fa.icon_svg('cart-shopping')
                    ),
                    ui.value_box(
                        'Revenue:', ui.output_ui('total_revenue'), showcase = fa.icon_svg('money-bill')
                    ),
                    ui.value_box(
                        'Avg Order Value:', ui.output_ui('avg_order_value'), showcase = fa.icon_svg('dollar-sign')
                    ),
                    ui.value_box(
                        'Avg Review Score:', ui.output_ui('avg_review_score'), showcase = fa.icon_svg('star')
                    ),
                    ui.value_box(
                        'Late-Delivery Rate:', ui.output_ui('late_delivery_rate'), showcase = fa.icon_svg('dolly')
                    )
                
                )
            ),
            # Timeseries
            ui.card(
                ui.card_header(
                    'Monthly Trends:', 
                    ui.input_radio_buttons('trend_metric', None, choices = {'orders': 'Orders', 'revenue': 'Revenue'}, selected = 'orders', inline = True),
                    class_ = 'd-flex justify-content-between align-items-center'
                ),
                output_widget('monthly_order_chart', height = '100%'),
                full_screen = False
            ),
            # Heatmap
            ui.card(
                ui.card_header('Top Purchase Times (orders by weekday and hour):'),
                output_widget('weekday_hour_heatmap', height = '100%'),
                full_screen = False
            )
        ),
        ui.nav_panel('Products & Sellers',
            ui.panel_title('...')
        ),
        ui.nav_panel('Delivery & Geolocation',
            ui.panel_title('...')
        ),
        ui.nav_panel('Customers, Payments & Reviews',
            ui.panel_title('...')
        ),
        ui.nav_panel('Data Quality',
            ui.panel_title('...')
        ),
        
        # Filters set
        sidebar =  ui.sidebar(
            # Purchase date (option 1)
            ui.input_date_range('purchase_date', 'Purchase Date', start = '2016-09-15', end = '2017-09-15', format = 'dd-mm-yyyy',
                min = min_purchase_date, max = max_purchase_date),
            # Purchase date (option 2)
            # ui.input_slider('purchase_date_slider', 'Purchase Date', min = min_purchase_date, max = max_purchase_date, 
            #     value = [min_purchase_date, max_purchase_date], time_format = '%B %d, %Y'),
            ui.input_select('status', 'Delivery Status', choices = status, selected = status, multiple = True),
            ui.input_select('customer_state', 'Customer State', choices = customer_state, selected = customer_state, multiple = True),
            ui.input_select('main_category', 'Product Category', choices = main_category, selected = main_category, multiple = True),
            ui.input_select('payment_type', 'Payment Type', choices = payment_type, selected = payment_type, multiple = True)
        ),
    title = 'Olist Orders Dashboard'
)         
