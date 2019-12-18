# oliver-spaceship-two


Switches   Switches
(Ard.1)    (Ard.2)
    \\     //
     \\   //
       | |
       | |  Serial Lines:  JSON messages from switches are read from here
       | |  
        V             
  SerialProcessor: Converts JSON message to audio queue control message (dict)        
       | |
       | |  audiocontroller.audio_queue
       | |  
        V             


Upper left switch next to pot
{u'action': u'switch', u'component': u'switch-06', u'value': u'1', u'element': u'n/a'}

Black Automotive switch (next to 'satellite link')
{u'action': u'switch', u'component': u'switch-30', u'value': u'1', u'element': u'n/a'}

6 switch panel:  Upper Left (Up is val = 2, middle is val = 0, down is val = 1)
{u'action': u'switch', u'component': u'switch-43-45', u'value': u'2', u'element': u'n/a'}

6 switch panel:  Upper middle (Up is val = 1, down is val=2, middle is val=):
{u'action': u'switch', u'component': u'switch-43-45', u'value': u'0', u'element': u'n/a'}


6 switch panel: Lower middle (Down is val=2, up is val=1, middle val=0)
{u'action': u'switch', u'component': u'switch-46-44', u'value': u'2', u'element': u'n/a'}

We need to keep switch44-45 offline due to wiring issues


Green LED toggle switch (next to shield generator):   val=1 is on
{u'action': u'switch', u'component': u'switch-22', u'value': u'1', u'element': u'n/a'}

Orange LED toggle switch (next to shield generator):   val=1 is on
{u'action': u'switch', u'component': u'switch-24', u'value': u'1', u'element': u'n/a'}

Green Pushbutton LED
{u'action': u'switch', u'component': u'switch-38', u'value': u'0', u'element': u'n/a'}

White Pushbutton LED
{u'action': u'switch', u'component': u'switch-40', u'value': u'0', u'element': u'n/a'}

Blue [LED out] Pushbutton LED
{u'action': u'switch', u'component': u'switch-39', u'value': u'0', u'element': u'n/a'}

Orange Pushbutton LED
{u'action': u'switch', u'component': u'switch-41', u'value': u'0', u'element': u'n/a'}



