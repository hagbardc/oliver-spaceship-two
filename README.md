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
