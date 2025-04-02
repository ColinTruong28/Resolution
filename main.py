import re
import requests
import cv2
from PIL import Image
import pytesseract
from datetime import date
import time
from kivy.properties import NumericProperty, ListProperty, StringProperty, Clock, BooleanProperty
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout


Window.size = (300, 540)
# Window.size = (450, 810)
# Config.set('graphics','width','300')
# Config.set('graphics','height','540')


Builder.load_file('PiProgressBar.kv')


navigation = """

ScreenManager:
    
    MenuScreen:
    MealHistoryScreen:
    DietRecordScreen:
    WorkoutRecordScreen:
    CaptureScreen:

# Home Screen Code -----------------------------------------------------------------------------------------------------

<MenuScreen>
    name: 'menu'
    MDNavigationLayout:
        ScreenManager:
            MDScreen:
                on_enter: self.app.update_history()
                md_bg_color: 254/255.0, 238/255.0, 203/255.0, 1
                ScrollView:
                    do_scroll_x: False
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: root.height * .025
                        adaptive_height: True
                        
                        # Main Cards In Home Screen
                        
                        # Filler Card for top of home
                        MDCard:
                            size_hint: None, None
                            size: root.height * .35, root.height * .35
                            pos_hint: {'center_x': .5}
                            padding_top: '20dp'
                            padding: '8dp'
                            md_bg_color: 254/255.0, 238/255.0, 203/255.0, 1
                            
                            MDFloatLayout:
                                # md_bg_color: 'black'
                                size_hint: None, None
                                size: root.height * .3, root.height * .3
                                Image:
                                    id: dino
                                    source: 'bunnyGif.gif'
                                    size_hint: 1,1
                                    pos_hint: {'center_x': .5, 'center_y': .5}
                                    anim_delay: .1
                                    anim_loop: 200
                                    
                                   
                                
                                
                        
                        
                        # Calorie Tracking Card 
                        MDCard:
                            id: 'calorieCard'
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 1,1,1,1
                            # line_color: 1,0,0,1
                            size_hint: None, None
                            size: root.width * 0.95, root.height * 0.15
                            pos_hint: {'center_x': .5}
                            opacity: app.card_opacity
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                # line_color: 1, 0,0,1
                                pos_hint: {'center_y': .55}
                                
                                MDLabel:
                                    text: 'Calories'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .35}
                                                                    
                            MDFloatLayout:
                                PiProgressBar:
                                    id: calorieBar
                                    size_hint: None, None
                                    size: root.height * .15, root.height * .15
                                    pos_hint: {'center_x': .6, 'center_y': .5}
                                    value: app.caloriePercent
                                
                                
                        # Protein Tracking Card
                        MDCard:
                            id: 'proteinCard'
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 1,1,1,1
                            # line_color: 1,0,0,1
                            size_hint: None, None
                            size: root.width * 0.95, root.height * 0.15
                            pos_hint: {'center_x': .5}
                            opacity: app.card_opacity
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                # line_color: 1, 0,0,1
                                pos_hint: {'center_y': .55}
                                MDLabel:
                                    text: 'Protein'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .35}
                                
                                                                  
                            MDFloatLayout:
                                PiProgressBar:
                                    id: proteinBar
                                    size_hint: None, None
                                    size: root.height * .15, root.height * .15
                                    pos_hint: {'center_x': .6, 'center_y': .5}
                                    value: app.proteinPercent
                                    
                        # Carb Tracking Card 
                        MDCard:
                            id: 'carbCard'
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 1,1,1,1
                            # line_color: 1,0,0,1
                            size_hint: None, None
                            size: root.width * 0.95, root.height * 0.15
                            pos_hint: {'center_x': .5}
                            opacity: app.card_opacity
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                # line_color: 1, 0,0,1
                                pos_hint: {'center_y': .55}
                                MDLabel:
                                    text: 'Carbs'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .35}
                                                                    
                            MDFloatLayout:
                                PiProgressBar:
                                    id: carbBar
                                    size_hint: None, None
                                    size: root.height * .15, root.height * .15
                                    pos_hint: {'center_x': .6, 'center_y': .5}
                                    value: app.carbPercent            
                        
                        
                        # WORKOUT CARD
                        MDCard:
                            id: Workout-Tracker
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 1,1,1,1
                            # line_color: 1,0,0,1
                            size_hint: None, None
                            size: root.width * 0.95, root.height * 0.15
                            pos_hint: {'center_x': .5}
                            opacity: app.card_opacity
                            
                            Image:
                                id: workout_bunny
                                source: 'bunny_biceps.gif' 
                                size_hint: .75, .75
                                anim_delay: .1
                                anim_loop: 2000
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                
                                
                                
                            MDLabel:
                                text: 'Arm Day'
                                theme_text_color: "Custom"
                                text_color: 222/255.0,176/255.0,46/255.0,1
                                font_size: root.height * .05
                                halign: 'center'
                                # pos_hint: {'center_x': .35}
                                # md_bg_color: 'red'
                                
                            # MDIconButton:
                            #     id: workout_button
                            #     icon: 'checkbox-blank-outline'
                            #     icon_size: root.height * .08
                            #     theme_icon_color: "Custom"
                            #     icon_color: 222/255.0,176/255.0,46/255.0,1
                            #     pos_hint: {'center_y': .5}
                                    
                        
                # Icon Button Navigation
                MDAnchorLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: root.height * .4
                    pos_hint: {'y': .05}
                    # md_bg_color: 'red'
                        
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: 0
                        # md_bg_color: 'red'
                        MDIconButton:
                            id: 'dumbbell_button'
                            icon: 'dumbbell'
                            icon_size: root.height * .06
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            pos_hint: {'center_x': .5, 'center_y': 0}
                            opacity: app.button_opacity
                            disabled: app.button_ability
                            md_bg_color: 1,1,1,1
                            on_press:
                                root.manager.current = 'workout'
                                app.toggle_pencil()
                            
                            
                        MDRelativeLayout:
                            size_hint: None, None
                            height: root.height * .1
                            width: root.width
                            # md_bg_color: 'red'
                            
                            MDIconButton:
                                id: food_button
                                icon: 'bowl-mix'
                                icon_size: root.height * .06
                                theme_icon_color: "Custom"
                                icon_color: 222/255.0,176/255.0,46/255.0,1
                                opacity: app.button_opacity
                                disabled: app.button_ability
                                pos_hint: {'center_x': .3}
                                md_bg_color: 1,1,1,1
                                on_press: 
                                    root.manager.current = 'diet'
                                    app.toggle_pencil()
                                
                            MDIconButton:
                                id: sleep_button
                                icon: 'sleep'
                                icon_size: root.height * .06
                                theme_icon_color: "Custom"
                                icon_color: 222/255.0,176/255.0,46/255.0,1
                                opacity: app.button_opacity
                                disabled: app.button_ability
                                pos_hint: {'center_x': .7}
                                md_bg_color: 1,1,1,1
                                on_press: app.respond()
                            
                            
                        MDIconButton:
                            id: 'pencil_button'
                            icon: app.button_icon
                            icon_size: root.height * .06
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            pos_hint: {'center_x': .5, 'center_y': .3} 
                            on_press: app.toggle_pencil()
                            md_bg_color: 1,1,1,1                        
                         

                        
        MDNavigationDrawer:
            id: nav_drawer
            size: root.width * .8, root.height
            
            
            
            ScrollView:

                MDList:
                    OneLineIconListItem:
                        text: "Profile"
                        
                        IconLeftWidget:
                            icon: "face-profile"
                                
                       
                                
                    OneLineIconListItem:
                        text: "Manage Goals"
                        
                        IconLeftWidget:
                            icon: "upload"
                            
                       
                    OneLineIconListItem:
                        text: "Logout"
                        
                        IconLeftWidget:
                            icon: "logout"
            


# Diet Recording Screen ------------------------------------------------------------------------------------------------

<DietRecordScreen>
    name: 'diet'
    MDNavigationLayout:
        ScreenManager:
            MDScreen:
                md_bg_color: 254/255.0, 238/255.0, 203/255.0, 1
                ScrollView:
                    do_scroll_x: False
  
                    MDBoxLayout:
                        id: 'main_diet_layout'
                        orientation: 'vertical'
                        spacing: 0
                        adaptive_height: True
                        
                                   
                        # Meal Name Input
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .1
                            pos_hint: {'center_x': .5}
                            spacing_top: root.height * .05
                        
                            MDTextField:
                                id: mealInput
                                hint_text: 'Meal Name'
                                halign: 'center'
                                size_hint: 1, None
                                font_size: root.height * .03
                                height: root.height * .06
                                background_color: 'white'
                                foreground_color: 222/255.0,176/255.0,46/255.0,1
                                cursor_color: 222/255.0,176/255.0,46/255.0,1
                                pos_hint: {'center_y': .5, 'center_x': .75}
                                halign: 'center'
                                multiline: False
                                on_text_validate: app.passToNextLine()
                                    
                        # Calorie Input
                        
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .15
                            pos_hint: {'center_x': .5}
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                # line_color: 1, 0,0,1
                                pos_hint: {'center_y': .5, 'center_x': 0}
                                size_hint: None, None
                                width: root.width * .5
                            
                                MDLabel:
                                    text: 'Calories'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .33}
                                    size_hint: None, None
                                    width: root.width * .5
                                                                    
                            MDFloatLayout:
                                # md_bg_color: 'red'
                                size_hint: None, None
                                size: root.width * .4, root.height * .15
                                FloatInput:
                                    id: calorieInput
                                    size_hint: None, None
                                    size: root.width * .25, root.height * .06
                                    height: root.height * .06
                                    background_color: 'white'
                                    foreground_color: 222/255.0,176/255.0,46/255.0,1
                                    cursor_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    pos_hint: {'center_y': .5, 'center_x': .4}
                                    base_direction: 'rtl'
                                    multiline: False
                                    on_text_validate: app.passToNextLine()

                                MDLabel:
                                    text: 'cal'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    halign: 'center'
                                    pos_hint: {'center_y': .5, 'center_x': .9}

                        
                        # Protein Input
                                    
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .15
                            pos_hint: {'center_x': .5}
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                # line_color: 1, 0,0,1
                                pos_hint: {'center_y': .5, 'center_x': 0}
                                size_hint: None, None
                                width: root.width * .5
                                MDLabel:
                                    text: 'Protein'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .33}
                                    size_hint: None, None
                                    width: root.width * .5
                                                                    
                            MDFloatLayout:
                                size_hint: None, None
                                size: root.width * .4, root.height * .15
                                FloatInput:
                                    id: proteinInput
                                    size_hint: None, None
                                    size: root.width * .25, root.height * .06
                                    height: root.height * .06
                                    background_color: 'white'
                                    foreground_color: 222/255.0,176/255.0,46/255.0,1
                                    cursor_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    pos_hint: {'center_y': .5, 'center_x': .4}
                                    base_direction: 'rtl'
                                    multiline: False
                                    on_text_validate: app.passToNextLine()
                                MDLabel:
                                    text: 'g'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    halign: 'center'
                                    pos_hint: {'center_y': .5, 'center_x': .9}
                        
                        
                        # Carb Input
                                    
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .15
                            pos_hint: {'center_x': .5}
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                pos_hint: {'center_y': .5, 'center_x': 0}
                                size_hint: None, None
                                width: root.width * .5
                                MDLabel:
                                    text: 'Carbs'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .33}
                                    size_hint: None, None
                                    width: root.width * .5
                                                                    
                            MDFloatLayout:
                                size_hint: None, None
                                size: root.width * .4, root.height * .15
                                FloatInput:
                                    id: carbInput
                                    size_hint: None, None
                                    size: root.width * .25, root.height * .06
                                    height: root.height * .06
                                    background_color: 'white'
                                    foreground_color: 222/255.0,176/255.0,46/255.0,1
                                    cursor_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    pos_hint: {'center_y': .5, 'center_x': .4}
                                    base_direction: 'rtl'
                                    multiline: False
                                    on_text_validate: app.passToNextLine()
                                MDLabel:
                                    text: 'g'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    halign: 'center'
                                    pos_hint: {'center_y': .5, 'center_x': .9}
                                    
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .15
                            pos_hint: {'center_x': .5}
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                pos_hint: {'center_y': .5, 'center_x': 0}
                                size_hint: None, None
                                width: root.width * .5
                                MDLabel:
                                    text: 'Fat'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .33}
                                    size_hint: None, None
                                    width: root.width * .5
                                                                    
                            MDFloatLayout:
                                size_hint: None, None
                                size: root.width * .4, root.height * .15
                                FloatInput:
                                    id: fatInput
                                    size_hint: None, None
                                    size: root.width * .25, root.height * .06
                                    height: root.height * .06
                                    background_color: 'white'
                                    foreground_color: 222/255.0,176/255.0,46/255.0,1
                                    cursor_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    pos_hint: {'center_y': .5, 'center_x': .4}
                                    base_direction: 'rtl'
                                    multiline: False
                                    on_text_validate: app.passToNextLine()
                                MDLabel:
                                    text: 'g'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    halign: 'center'
                                    pos_hint: {'center_y': .5, 'center_x': .9}
                                    
                        MDCard:
                            orientation: 'horizontal'
                            font: 'Roboto-ThinItalic'
                            md_bg_color: 0,0,0,0
                            size_hint: None, None
                            size: root.width * .92, root.height * .15
                            pos_hint: {'center_x': .5}
                            
                            
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding_left: '.5dp'
                                pos_hint: {'center_y': .5, 'center_x': 0}
                                size_hint: None, None
                                width: root.width * .5
                                MDLabel:
                                    text: 'Sodium'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .035
                                    halign: 'center'
                                    pos_hint: {'center_x': .33}
                                    size_hint: None, None
                                    width: root.width * .5
                                                                    
                            MDFloatLayout:
                                size_hint: None, None
                                size: root.width * .4, root.height * .15
                                FloatInput:
                                    id: sodiumInput
                                    size_hint: None, None
                                    size: root.width * .25, root.height * .06
                                    height: root.height * .06
                                    background_color: 'white'
                                    foreground_color: 222/255.0,176/255.0,46/255.0,1
                                    cursor_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    pos_hint: {'center_y': .5, 'center_x': .4}
                                    base_direction: 'rtl'
                                    multiline: False
                                    on_text_validate: app.updateCard()
                                MDLabel:
                                    text: 'g'
                                    theme_text_color: "Custom"
                                    text_color: 222/255.0,176/255.0,46/255.0,1
                                    font_size: root.height * .03
                                    halign: 'center'
                                    pos_hint: {'center_y': .5, 'center_x': .9}
                        
                        
                # MDDropDownItem:
                #     id: dropdown_favorites
                #     pos_hint: {'center_x': .5, 'center_y': .6}
                #     items: root.favoriteMeals
                #     dropdown_bg: 1,1,1,1        
                            
                # Icon Button Navigation
                MDAnchorLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: root.height * .08
                    pos_hint: {'y': 0}
                    # md_bg_color: 'red'
                        
                    MDBoxLayout:
                        width: root.width
                        
                        MDIconButton:
                            id: camera_button
                            icon_size: root.height * .06
                            size_hint: None, None
                            size: root.width * .2, root.width * .2
                            icon: 'camera-enhance-outline'
                            pos_hint: {'center_x': .35}
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            on_press: root.manager.current = 'capture'
                                    
                        MDIconButton:
                            id: history_button
                            icon_size: root.height * .06
                            size_hint: None, None
                            size: root.width * .2, root.width * .2
                            icon: 'backup-restore'
                            pos_hint: {'center_x': .5}
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            on_press: root.manager.current = 'mealHistory'
                            
                        MDIconButton:
                            id: upload_button
                            icon_size: root.height * .12
                            size_hint: None, None
                            size: root.width * .2, root.width * .2
                            icon: 'upload'
                            pos_hint: {'center_x': .2}
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            on_press: app.updateCard()
                                        
                        MDIconButton:
                            id: diet_SDB
                            icon_size: root.height * .06
                            size_hint: None, None
                            size: root.width * .2, root.width * .2
                            icon: 'home'
                            pos_hint: {'center_x': .65}
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                            on_press: root.manager.current = 'menu'
                                                
                        MDIconButton:
                            id: favorite_button
                            icon_size: root.height * .06
                            size_hint: None, None
                            size: root.width * .2, root.width * .2
                            icon: 'star-shooting-outline'
                            pos_hint: {'center_x': .75}
                            theme_icon_color: "Custom"
                            icon_color: 222/255.0,176/255.0,46/255.0,1
                    
                        
                            
    
        MDNavigationDrawer:
            id: nav_drawer
            size: root.width * .8, root.height
                
                
                
            ScrollView:
    
                MDList:
                    OneLineIconListItem:
                        text: "Profile"
                            
                        IconLeftWidget:
                            icon: "face-profile"
                                    
                           
                                    
                    OneLineIconListItem:
                        text: "Home"
                            
                        IconLeftWidget:
                            icon: "home"
                            on_press: root.manager.current = 'menu'
                                
                           
                    OneLineIconListItem:
                        text: "Logout"
                            
                        IconLeftWidget:
                            icon: "logout"        

# Meal History Screen --------------------------------------------------------------------------------------------------------------------------------------------

<MealHistoryScreen>
    name: 'mealHistory'
    ScreenManager:
        MDScreen:
            md_bg_color: 240/255.0, 240/255.0, 240/255.0, 1
            ScrollView:        
                MDBoxLayout:
                    id: main_meal_history_layout
                    orientation: 'vertical'
                    spacing: root.height * .02
                    adaptive_height: True
                    
                    MDLabel:
                        font: 'Roboto-ThinItalic'
                        font_size: root.height * .06
                        size_hint: None, None
                        size: root.width, root.height * .1
                        halign: 'center'
                        text: 'History'
                    
                    
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_1
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_1
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_1
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_1
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_2
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_2
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_2
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_2
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_3
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_3
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_3
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_3
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_4
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_4
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_4
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_4
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_5
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_5
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_5
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_5
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_6
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_6
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_6
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_6
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_7
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_7
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_7
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_7
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_8
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_8
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_8
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_8
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                        
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_9
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_9
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_9
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_9
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                    
                                    
                    MDCard:
                        orientation: 'horizontal'
                        font: 'Roboto-ThinItalic'
                        md_bg_color: 1,1,1,1
                        size_hint: None, None
                        size: root.width * .98, root.height * .18
                        pos_hint: {'center_x': .5}
                        
                        MDBoxLayout:
                            
                            MDBoxLayout:
                                size_hint: None, None
                                size: root.width * .8, root.height * .09
                                orientation: 'vertical'
                                
                                MDBoxLayout
                                    size_hint: None, None
                                    size: root.width * .7, root.height * .09
                                    pos_hint: {'center_x': .5}
                                    MDLabel:
                                        id: log_mealName_10
                                        font_size: root.height * .03
                                        text: 'Insert Meal Name'
                                        pos_hint: {'center_y': .5}
                                        # md_bg_color: 'red'
                                    
                                MDBoxLayout:
                                    size_hint: None, None
                                    size: root.width * .7, root.height* .09
                                    pos_hint: {'center_x': .5}
                                    
                                    MDLabel:
                                        id: log_cal_10
                                        text: 'Insert Calories'
                                        font_size: root.height * .02
                                        # md_bg_color: 'red'
                                    MDLabel:
                                        id: log_protein_10
                                        text: 'Insert Protein'
                                        font_size: root.height * .02
                                        # md_bg_color: 'blue'
                                    MDLabel:
                                        id: log_carbs_10
                                        text: 'Insert Carbs'
                                        font_size: root.height * .02
                                
                            MDBoxLayout:
                                size_hint: None, None
                                orientation: 'vertical'
                                spacing: 0
                                
                                MDIconButton:
                                    icon: 'pencil-box'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09
                                MDIconButton:
                                    icon: 'star'
                                    icon_size: root.height * .04
                                    size_hint: None, None
                                    size: root.height * .09, root.height * .09

    MDNavigationDrawer:
        id: nav_drawer
        size: root.width * .8, root.height
            
            
            
        ScrollView:

            MDList:
                OneLineIconListItem:
                    text: "Profile"
                        
                    IconLeftWidget:
                        icon: "face-profile"
                                
                       
                                
                OneLineIconListItem:
                    text: "Home"
                        
                    IconLeftWidget:
                        icon: "home"
                        on_press: root.manager.current = 'menu'
                            
                       
                OneLineIconListItem:
                    text: "Logout"
                        
                    IconLeftWidget:
                        icon: "logout"
                        
# Capture Screen ----------------------------------------------------------------------------------------------------------------------------------------------------------


<CaptureScreen>
    name: 'capture'
    ScreenManager:
        MDScreen:
            MDBoxLayout:
                orientation: 'vertical'

                Camera:
                    id: camera
                    play: True
                    size: Window.size

                ToggleButton:
                    text: 'Play'
                    on_press: camera.play = not camera.play
                    size_hint_y: None
                    height: '48dp'
                    
                Button: 
                    text: 'Capture'
                    size_hint_y: None
                    height: '48dp'
                    on_press: app.capture()
                    
                    
# Workout Screen ----------------------------------------------------------------------------------------------------------------------------------------------------------
<WorkoutRecordScreen>    
    name: 'workout'
    ScreenManager:
        MDScreen:
            ScrollView:
                do_scroll_x: False
                
                MDBoxLayout:
                    orientation: 'vertical'
                
                
            MDAnchorLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: root.height * .08
                pos_hint: {'y': 0}
                # md_bg_color: 'red'
                    
                MDBoxLayout:
                    width: root.width
                    
                    MDIconButton:
                        id: camera_button
                        icon_size: root.height * .06
                        size_hint: None, None
                        size: root.width * .2, root.width * .2
                        icon: 'camera-enhance-outline'
                        pos_hint: {'center_x': .5}
                        theme_icon_color: "Custom"
                        icon_color: 222/255.0,176/255.0,46/255.0,1
                        on_press: root.manager.current = 'capture'
"""

class MenuScreen(Screen):
    pass

class MealHistoryScreen(Screen):
    pass

class DietRecordScreen(Screen):
    favoriteMeals = [f"Item {i}" for i in range(50)]
    # def on_kv_post(self, base_widget):
    #     super(DietRecordScreen, self).on_kv_post(base_widget)
    pass

class WorkoutRecordScreen(Screen):
    pass

class CaptureScreen(Screen):
    pass

class FloatInput(MDTextField):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)

class PiProgressBar(AnchorLayout):
    text = StringProperty("0%")
    set_value = NumericProperty(0)
    value = NumericProperty(0)
    bar_color = ListProperty([222/255.0,176/255.0,46/255.0])
    bar_width = NumericProperty(10)
    counter = 0
    duration = NumericProperty(.5)


    def __init__(self, **kwargs):
        super(PiProgressBar, self).__init__(**kwargs)
        Clock.schedule_interval(self.animate, 5)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter, self.duration/self.value)

    def percent_counter(self, *args):
        if self.counter < self.value:
            self.counter += 1
            self.text = f"{self.counter}%"
            self.set_value = self.counter
        else:
            Clock.unschedule(self.percent_counter)



# screenManager.add_widget(DietRecordScreen(item1))

class DemoApp(MDApp):



    firebaseURL = "https://resolutionapp-3012d-default-rtdb.firebaseio.com/"
    userMealList = requests.get(url = firebaseURL + 'Colin/.json').text
    if userMealList.find(f"{date.today()}") == -1:
        nutritionOfToday = {"Daily Counts": {"Calorie Count": .001,
                                             "Carb Count": .001,
                                             "Protein Count": .001,
                                             "Fat Count": .001,
                                             "Sodium Count": .001}}
        requests.patch(url=firebaseURL + "Colin/.json", json=nutritionOfToday)

    lastTenMeals = []
    for i in range(10):
        meal = userMealList[userMealList.rfind("Calories") - 12:userMealList.rfind("Daily Counts")]
        meal = meal.replace('"','')
        meal = meal.replace(",", '')
        meal = meal.replace("}", '')
        meal = meal.replace("{", '')
        lastTenMeals.append(meal)
        userMealList = userMealList[:userMealList.rfind("Calories")]


    # Nutrition Counts
    calorieCount = float(requests.get(url = firebaseURL + "Colin/Daily Counts/Calorie Count.json").text)
    proteinCount = float(requests.get(url = firebaseURL + "Colin/Daily Counts/Protein Count.json").text)
    carbCount = float(requests.get(url = firebaseURL + "Colin/Daily Counts/Carb Count.json").text)
    fatCount = float(requests.get(url = firebaseURL + "Colin/Daily Counts/Fat Count.json").text)
    sodiumCount = float(requests.get(url = firebaseURL + "Colin/Daily Counts/Sodium Count.json").text)


    requests.patch(url = firebaseURL + 'Colin/Daily Counts/Sodium Count.json', json = 5)


    # Nutrition Goals
    calorieGoal = 3000
    proteinGoal = 145
    carbGoal = 250

    # Nutrition Percentage

    caloriePercent = calorieCount / calorieGoal * 100
    proteinPercent = proteinCount/proteinGoal * 100
    carbPercent = carbCount / carbGoal * 100

    button_opacity = NumericProperty(0)
    card_opacity = NumericProperty(1)
    button_ability = BooleanProperty(True)
    button_icon = StringProperty('lead-pencil')


    # Favorite Meals List
    favoriteMeals = [f"Item {i}" for i in range(50)]

    def build(self):
        self.theme_cls.primary_palette = 'Amber'
        screen = Builder.load_string(navigation)


        return screen

    def capture(self):
        camera = self.root.get_screen("capture").ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image_path = "IMG_{}.png".format(timestr)
        camera.export_to_png(image_path)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        processed_image_path = 'processed_label.png'
        cv2.imwrite('processed_label.png', thresh)
        text = pytesseract.image_to_string(Image.open(processed_image_path))

        print(text)

    def update_history(self):
        for j in range(11):
            info = self.lastTenMeals[j - 1]

            mealName = info[info.find("Meal Name:")+10:info.find("Protein")]
            calories = info[info.find("Calories:")+9:info.find("Carbs")]
            protein = info[info.find("Protein:")+8:info.find("zzz")]
            carbs = info[info.find("Carbs:")+6:info.find("Meal Name")]

            if j == 1:
                self.root.get_screen("mealHistory").ids.log_mealName_1.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_1.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_1.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_1.text = f"Carbs: {carbs}"
            if j == 2:
                self.root.get_screen("mealHistory").ids.log_mealName_2.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_2.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_2.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_2.text = f"Carbs: {carbs}"
            if j == 3:
                self.root.get_screen("mealHistory").ids.log_mealName_3.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_3.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_3.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_3.text = f"Carbs: {carbs}"
            if j == 4:
                self.root.get_screen("mealHistory").ids.log_mealName_4.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_4.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_4.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_4.text = f"Carbs: {carbs}"
            if j == 5:
                self.root.get_screen("mealHistory").ids.log_mealName_5.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_5.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_5.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_5.text = f"Carbs: {carbs}"
            if j == 6:
                self.root.get_screen("mealHistory").ids.log_mealName_6.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_6.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_6.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_6.text = f"Carbs: {carbs}"
            if j == 7:
                self.root.get_screen("mealHistory").ids.log_mealName_7.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_7.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_7.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_7.text = f"Carbs: {carbs}"
            if j == 8:
                self.root.get_screen("mealHistory").ids.log_mealName_8.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_8.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_8.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_8.text = f"Carbs: {carbs}"
            if j == 9:
                self.root.get_screen("mealHistory").ids.log_mealName_9.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_9.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_9.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_9.text = f"Carbs: {carbs}"
            if j == 10:
                self.root.get_screen("mealHistory").ids.log_mealName_10.text = mealName
                self.root.get_screen("mealHistory").ids.log_cal_10.text = f"Cal: {calories}"
                self.root.get_screen("mealHistory").ids.log_protein_10.text = f"Protein: {protein}"
                self.root.get_screen("mealHistory").ids.log_carbs_10.text = f"Carbs: {carbs}"

    def toggle_pencil(self):

        self.update_history()

        if self.button_opacity == 0:
            self.button_opacity = 1
            self.button_ability = False
            self.button_icon = 'sword-cross'
            self.card_opacity = .5


        elif self.button_opacity == 1:
            self.button_opacity = 0
            self.button_icon = 'lead-pencil'
            self.card_opacity = 1
            self.button_ability = True



    def respond(self):
        print('did it work?')

    def updateCard(self):

        print(requests.get("https://resolutionapp-3012d-default-rtdb.firebaseio.com/Colin/.json").text)

        self.update_history()

        if self.root.get_screen('diet').ids.mealInput.text != '':
            if self.root.get_screen('diet').ids.calorieInput.text != '':
                self.calorieCount += int(self.root.get_screen('diet').ids.calorieInput.text)
                requests.put(url = self.firebaseURL + 'Colin/Daily Counts/Calorie Count.json', json = self.calorieCount)
            if self.root.get_screen('diet').ids.proteinInput.text != '':
                self.proteinCount += int(self.root.get_screen('diet').ids.proteinInput.text)
                requests.put(url = self.firebaseURL + 'Colin/Daily Counts/Protein Count.json', json = self.proteinCount)
            if self.root.get_screen('diet').ids.carbInput.text != '':
                self.carbCount += int(self.root.get_screen('diet').ids.carbInput.text)
                requests.put(url=self.firebaseURL + 'Colin/Daily Counts/Carb Count.json', json = self.carbCount)



            self.root.get_screen('menu').ids.calorieBar.value = self.calorieCount/self.calorieGoal * 100
            self.root.get_screen('menu').ids.proteinBar.value = self.proteinCount/self.proteinGoal * 100
            self.root.get_screen('menu').ids.carbBar.value = self.carbCount/self.carbGoal * 100

            currentTime = time.strftime("%H:%M:%S" ,time.localtime())
            nutrition_data = {f"{currentTime}": {"Meal Name": self.root.get_screen('diet').ids.mealInput.text,
                              "Protein": int(self.root.get_screen('diet').ids.proteinInput.text),
                              "Carbs": int(self.root.get_screen('diet').ids.carbInput.text),
                              "Calories": int(self.root.get_screen('diet').ids.calorieInput.text),
                              "zzz": 0}}
            if requests.get(url = "https://resolutionapp-3012d-default-rtdb.firebaseio.com/" + 'Colin/') != date.today():
                requests.patch(url = "https://resolutionapp-3012d-default-rtdb.firebaseio.com/", json = {f"{date.today()}":'nutrition_data'})
            requests.post(url = "https://resolutionapp-3012d-default-rtdb.firebaseio.com/" + 'Colin/' + f"{date.today()}" + '.json', json = nutrition_data)

        self.root.get_screen('diet').ids.mealInput.text = ""
        self.root.get_screen('diet').ids.calorieInput.text = ""
        self.root.get_screen('diet').ids.proteinInput.text = ""
        self.root.get_screen('diet').ids.carbInput.text = ""
        self.root.get_screen('diet').ids.fatInput.text = ""
        self.root.get_screen('diet').ids.sodiumInput.text = ""

    def passToNextLine(self):

        if self.root.get_screen('diet').ids.calorieInput.focus:
            self.root.get_screen('diet').ids.calorieInput.focus = False
            self.root.get_screen('diet').ids.proteinInput.focus = True
        elif self.root.get_screen('diet').ids.proteinInput.focus:
            self.root.get_screen('diet').ids.proteinInput.focus = False
            self.root.get_screen('diet').ids.carbInput.focus = True
        elif self.root.get_screen('diet').ids.carbInput.focus:
            self.root.get_screen('diet').ids.carbInput.focus = False
            self.root.get_screen('diet').ids.fatInput.focus = True
        elif self.root.get_screen('diet').ids.fatInput.focus:
            self.root.get_screen('diet').ids.fatInput.focus = False
            self.root.get_screen('diet').ids.sodiumInput.focus = True
        elif self.root.get_screen('diet').ids.mealInput.focus:
            self.root.get_screen('diet').ids.mealInput.focus = False
            self.root.get_screen('diet').ids.calorieInput.focus = True





if __name__ == "__main__":
    DemoApp().run()