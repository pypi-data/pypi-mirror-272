import ipywidgets as widgets
from guava3.entities import BaseChat, BaseEntity
from guava3.conversation import Conversation
from guava3.implementations.images import GUAVA3_LOGO, ROBOT_SVG, USER_SVG, MAGNIFYING_SVG
import sys
import markdown
import json
import os
from IPython.display import display
import time
import base64



# define all the sections
# os.chdir('..')

def display_widgets_frontend(team_config_map):

    team_options = team_config_map.keys()

    # Create a dropdown widget
    dropdown = widgets.Dropdown(
        options=team_options,
        description='Select:',
        disabled=False
    )

    # Create a button widget
    reset_button = widgets.Button(
        description='Reset',
        button_style='',  # Style of the button
        tooltip='Reset conversation',
        icon='undo',  # FontAwesome icon name
        layout=widgets.Layout(width='150px')  # Adjusting width of the button
    )

    # Create a stop button widget
    stop_button = widgets.Button(
        description='Stop',
        button_style='',  # Style of the button
        tooltip='Stop conversation',
        icon='stop',  # FontAwesome icon name
        layout=widgets.Layout(width='150px')  # Adjusting width of the button
    )


    # Use a VBox to dynamically add outputs
    messages_box = widgets.VBox()
    messages_box.layout = widgets.Layout(flex_flow='column-reverse', width='100%', max_width='1000px', height='500px', overflow_y='auto')


    logo = widgets.HTML()
    logo.value = f'<img src="data:image/png;base64,{GUAVA3_LOGO}" alt="logo" style="width:80px;">'

    # Create the text input widget
    text_input = widgets.Text(
        placeholder='Type your message here...',
        layout=widgets.Layout(width='80%')  # Adjusting width of the text input
    )

    # Create a button widget
    send_button = widgets.Button(
        description='Send',
        button_style='',  # Style of the button
        tooltip='Send your message',
        icon='paper-plane',  # FontAwesome icon name
        layout=widgets.Layout(width='20%')  # Adjusting width of the button
    )

    horizontal_divider = widgets.HTML('<hr style="height:2px;border-width:0;color:gray;background-color:gray;margin-top:5px;margin-bottom:5px"/>')
    vertical_divider = widgets.HTML(  
        '<div style="border-left: 2px solid gray; height: 100%;"></div>',  
        layout=widgets.Layout(width='2px')  
    )  
    
    # Use an HBox to arrange the text input and send button horizontally
    input_box = widgets.HBox([text_input, send_button], layout=widgets.Layout(width='100%', max_width='1000px'))

    # create header with dropdown and reset
    header = widgets.HBox([logo, dropdown, reset_button])
    header.layout.align_items = 'center'
    header.layout.justify_content = 'flex-start'

    # Dropdown for selecting the database type  
    db_selector = widgets.Dropdown(  
        options=['Databricks'],  
        value='Databricks',  
        description='DBMS',  
    )  

    # Text input for the host  
    server_input = widgets.Text(  
        placeholder='Enter server hostname',  
        description='Server',  
    )  

    # Text input for the user  
    http_path = widgets.Text(  
        placeholder='Enter Path',  
        description='Path',  
    )  

    # Password input for the password  
    password_input = widgets.Password(  
        placeholder='Enter password/token',  
        description='Password',  
    )  

    # Button for initiating the connection  
    connect_button = widgets.Button(  
        description='Connect',  
        button_style='Success', # 'Success', 'Info', 'Warning', 'Danger' or ''  
    )  

    db_header = widgets.HTML(value = '<strong>DB Connection</strong>', layout = widgets.Layout(align_items = 'center'))

    output = widgets.Output()
    # Display the UI elements  
    db_ui_elements = widgets.VBox([db_header, db_selector, server_input, http_path, password_input, connect_button, output], layout = widgets.Layout(width = '30%', align_items = 'center', justify_content='center'))  

    # Use a VBox to stack tall the sections
    chat_box = widgets.VBox([header, horizontal_divider, messages_box, input_box], layout = widgets.Layout(width = '70%'))

    chat_display = widgets.HBox([chat_box, vertical_divider, db_ui_elements], layout = widgets.Layout(min_height='100px'))


    # auxiliary functions


    def send_message():
        """Function to display the message and clear the input."""
        conv.run(text_input.value)  # Display the message


    def get_icon(name):
        icon_dict = {
            "assistant": ROBOT_SVG,
            "data_analyst": MAGNIFYING_SVG,
            "user": USER_SVG,
            "me": USER_SVG
        }

        icon = icon_dict.get(name, ROBOT_SVG)

        return icon

    def create_message_box(name):
        icon = get_icon(name)
        icon_html = widgets.HTML()  
        icon_html.value = f'<img src="data:image/svg+xml;base64,{icon}" alt="{name}" style="width:20px;height:20px;">'
        icon_html.layout.min_width = '40px'  # Adjust the width as needed

        text_html = widgets.HTML()
        
        new_message = widgets.HBox([icon_html, text_html])
        new_message.layout.overflow = 'visible'
        new_message.layout.align_items = 'baseline'
        
        return new_message

        

    # defining button actions


    # send button
    def on_send_button_clicked(b):
        """Handle the send button clicks."""
        if text_input.value.strip():  # Ensure the message is not empty
            send_message()

    send_button.on_click(on_send_button_clicked)

    # enter key press
    def on_text_submit(change):
        """Handle the enter key press in the text input."""
        if text_input.value.strip():  # Ensure the message is not empty
            send_message()

    text_input.on_submit(on_text_submit)

    # reset button
    def on_click_reset(b):
        global conv
        conv = Conversation(team_config_map[dropdown.value])
        messages_box.children = []
        

    reset_button.on_click(on_click_reset)

    # def on_click_stop(b):
    #     global conv
    #     conv = Conversation(team_config_map[dropdown.value])
    #     if conv.is_running:
    #         conv.is_running = False
    #     else:
    #         conv.is_running = True
            
    # stop_button.on_click(on_click_stop)

    def on_click_db_connection(b):

        db_dict = {"Databricks":{"server_hostname": '', "http_path": ''}}
        db_dict["Databricks"]["server_hostname"] = server_input.value
        db_dict["Databricks"]["http_path"] = http_path.value
        os.environ["DB_PASSWORD_DATABRICKS"] = password_input.value


        with open('./resources/db_params.json', 'w') as db_file:
            json.dump(db_dict, db_file, indent = 4)
        
        with output:
            output.clear_output()
            success_message = widgets.HTML("<div style='color: green;'>Success: Connected to the database!</div>")
            display(success_message)
            time.sleep(10)
            output.clear_output()

    connect_button.on_click(on_click_db_connection)

    # team selection
    def on_selection_change(change):
        global conv
        # Check if the change is in 'new' value
        if change['type'] == 'change' and change['name'] == 'value':
            conv = Conversation(team_config_map[change['new']])
            messages_box.children = []

    dropdown.observe(on_selection_change, names='value')


    import re

    def find_text_and_images(text):
        # Regex pattern to match the Markdown image syntax with base64 data
        pattern = r'!\[.*?\]\(data:image/.*?;base64,([a-zA-Z0-9+/=]+)\)'
        
        # Split the text by the pattern but keep the delimiters (the images)
        parts = re.split(pattern, text)
        
        # Prepare the list to hold dictionaries of text and image entries
        result = []
        
        # Iterate over parts to determine if they are images or text
        for part in parts:
            # Check if the part matches the base64 string
            if re.fullmatch(r'[a-zA-Z0-9+/=]+', part) and part != text:
                # This part is an image's base64 string
                result.append({"type": "image", "string": part})
            else:
                # This part is text
                result.append({"type": "text", "string": part})
        
        return result


    def b64image_to_widget(base64_image):
        # Decode the base64 string
        image_bytes = base64.b64decode(base64_image)

        # Create an Image widget with the decoded image data
        image_widget = widgets.Image(
            value=image_bytes,
            format='png',  
        )

        # Assuming you have a VBox named messages_box and you want to set the image
        # as the second child of the first child of this VBox
        image_widget.layout.max_width = '500px'
        return image_widget



    # connect the backend

    def on_new_token(self, token):
        messages_box.children[0].children[1].value = markdown.markdown(self.resp.replace('\n', '  \n') + "▌", extensions=['tables'])

    def on_thought_start(self):
        text_input.value = ""
        new_message = create_message_box(self.name)
        messages_box.children = [new_message] + list(messages_box.children)

    def on_thought_end(self):
        thought = self.thought.replace('\n', '  \n')
        fragments = find_text_and_images(thought)
        
        messages_box.children[0].children = [messages_box.children[0].children[0], widgets.VBox()]
        for fragment in fragments:
            if fragment["type"] == 'image':
                messages_box.children[0].children[1].children = list(messages_box.children[0].children[1].children) + [b64image_to_widget(fragment['string'])]
            else:
                messages_box.children[0].children[1].children = list(messages_box.children[0].children[1].children) + [widgets.HTML(markdown.markdown(fragment['string'], extensions=['tables']))]
                

        # messages_box.children[0].children[1].value = markdown.markdown(thought, extensions=['tables'])
        

    BaseChat.on_new_token = on_new_token
    BaseEntity.on_thought_start = on_thought_start
    BaseEntity.on_thought_end = on_thought_end


    conv = Conversation(team_config_map[dropdown.value])

    display(chat_display)

    return